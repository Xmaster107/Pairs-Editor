import os
import shutil

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

if __name__ == "__main__":
    try:
        # Запрашиваем путь к исходной папке с проверкой
        source_folder = get_valid_folder_path("Введите путь к папке с изображениями: ")

        # Ввод названия новой папки
        target_folder = input("Введите название новой папки: ")

        # Если целевая папка не указана как абсолютный путь, создаем её внутри исходной папки
        if not os.path.isabs(target_folder):
            target_folder = os.path.join(source_folder, target_folder)

        # Обрабатываем пары изображений
        process_image_pairs(source_folder, target_folder)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"Ошибка: {e}")