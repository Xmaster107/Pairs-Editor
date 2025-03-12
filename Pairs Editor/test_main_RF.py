import os
import shutil
import pytest
from unittest.mock import patch
import threading


# Функции из main_RF (рефакторированный код)

def get_valid_folder_path(prompt):
    """
    Запрашивает у пользователя путь к папке и проверяет его корректность.
    Возвращает путь, если папка существует.
    """
    while True:
        folder_path = input(prompt)
        if os.path.exists(folder_path):
            return folder_path
        print(f"Ошибка: Папка '{folder_path}' не найдена. Пожалуйста, введите путь ещё раз.")


def process_image_pairs(source_folder, target_folder):
    try:
        # Создаем целевую папку, если она не существует
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # Словарь для хранения пар изображений
        pairs = {}

        # Сначала собираем все файлы, которые могут быть частью пары
        for filename in os.listdir(source_folder):
            # Пропускаем файлы, которые не являются изображениями
            if not filename.endswith('.png'):
                continue

            # Разделяем имя файла по символу '_'
            parts = filename.split('_')
            if len(parts) < 2:
                print(f"Пропуск файла {filename}: неверный формат имени")
                continue

            # Извлекаем индекс пары
            pair_index = parts[0]

            # Добавляем файл в словарь пар
            if pair_index not in pairs:
                pairs[pair_index] = []
            pairs[pair_index].append(filename)

        # Обрабатываем пары изображений
        for pair_index, filenames in pairs.items():
            # Пропускаем пары, если их не 2
            if len(filenames) != 2:
                print(f"Пропуск пары {pair_index}: найдено {len(filenames)} изображений вместо 2")
                continue

            # Проверяем, есть ли в названиях файлов '-'
            skip_pair = False
            for filename in filenames:
                if '-' in filename:
                    print(f"Пропуск пары {pair_index}: файл {filename} содержит '-'")
                    skip_pair = True
                    break

            if skip_pair:
                continue

            # Создаем папку для пары внутри целевой папки
            pair_folder = os.path.join(target_folder, pair_index)
            os.makedirs(pair_folder, exist_ok=True)

            # Копируем изображения в новую папку
            for filename in filenames:
                src_path = os.path.join(source_folder, filename)
                dst_path = os.path.join(pair_folder, filename)
                shutil.copy2(src_path, dst_path)

            print(f"Создана папка {pair_index} с изображениями: {', '.join(filenames)}")

    except PermissionError:
        print(f"Ошибка: Нет прав доступа для создания папки или копирования файлов.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


# Тесты для функций

def test_get_valid_folder_path_valid():
    # Мокируем ввод пользователя, возвращаем правильный путь сразу
    with patch('builtins.input', return_value="valid_path"), \
            patch('os.path.exists', return_value=True):  # Мокируем существование пути
        result = get_valid_folder_path("Введите путь к папке: ")
        assert result == "valid_path"


def test_get_valid_folder_path_invalid():
    # Мокируем путь, который не существует, и возвращаем правильный путь после нескольких попыток
    with patch('builtins.input', side_effect=["invalid_path", "valid_path"]), \
            patch('os.path.exists', side_effect=lambda path: path == "valid_path"):
        result = get_valid_folder_path("Введите путь к папке: ")
        assert result == "valid_path"


def test_process_image_pairs_success():
    # Мокируем операции с папками и файлами, чтобы избежать их реального создания
    with patch('os.makedirs') as mock_makedirs, \
            patch('shutil.copy2') as mock_copy2, \
            patch('os.path.exists', return_value=True), \
            patch('os.listdir', return_value=['pair1_image1.png', 'pair1_image2.png']):
        source_folder = "test_source"
        target_folder = "test_target"

        # Запускаем функцию, она будет использовать мокированные функции
        process_image_pairs(source_folder, target_folder)

        # Проверяем, что папка была создана и файлы скопированы
        mock_makedirs.assert_called_with(os.path.join(target_folder, "pair1"), exist_ok=True)
        mock_copy2.assert_any_call(os.path.join(source_folder, 'pair1_image1.png'),
                                   os.path.join(target_folder, "pair1", 'pair1_image1.png'))
        mock_copy2.assert_any_call(os.path.join(source_folder, 'pair1_image2.png'),
                                   os.path.join(target_folder, "pair1", 'pair1_image2.png'))


def test_process_image_pairs_invalid_file():
    with patch('os.makedirs') as mock_makedirs, \
            patch('shutil.copy2') as mock_copy2, \
            patch('os.path.exists', return_value=True), \
            patch('os.listdir', return_value=['pair1_image1.png']):
        source_folder = "test_source"
        target_folder = "test_target"

        # Запускаем функцию с неполной парой изображений
        process_image_pairs(source_folder, target_folder)

        # Проверка того, что папка не была создана
        mock_makedirs.assert_not_called()
        mock_copy2.assert_not_called()


# Таймаут для тестов с использованием threading.Timer

def timeout_test():
    raise TimeoutError("Тест занял слишком много времени.")


# Устанавливаем таймаут в 10 секунд
def run_with_timeout():
    timer = threading.Timer(10, timeout_test)
    timer.start()

    try:
        pytest.main()  # Запуск тестов
    finally:
        timer.cancel()  # Отменяем таймер после выполнения тестов


# Запускаем тесты с таймаутом
run_with_timeout()
