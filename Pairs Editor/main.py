import os as o, shutil as s
def p(i, t):
    try:
        if not o.path.exists(i): raise FileNotFoundError(f"Папка '{i}' не найдена.")
        if not o.path.exists(t): o.makedirs(t)
        d = {}
        for f in o.listdir(i):
            if not f.endswith('.png'): continue
            p = f.split('_')
            if len(p) < 2: print(f"Пропуск файла {f}: неверный формат имени"); continue
            n = p[0]
            if n not in d: d[n] = []
            d[n].append(f)
        for k, v in d.items():
            if len(v) != 2: print(f"Пропуск пары {k}: найдено {len(v)} изображений вместо 2"); continue
            sk = False
            for f in v:
                if '-' in f: print(f"Пропуск пары {k}: файл {f} содержит '-'"); sk = True; break
            if sk: continue
            pf = o.path.join(t, k)
            o.makedirs(pf, exist_ok=True)
            for f in v:
                sp = o.path.join(i, f)
                dp = o.path.join(pf, f)
                s.copy2(sp, dp)
            print(f"Создана папка {k} с изображениями: {', '.join(v)}")
    except Exception as e: print(f"Ошибка: {e}")
def g(p):
    while True:
        fp = input(p)
        if o.path.exists(fp): return fp
        print(f"Ошибка: Папка '{fp}' не найдена. Пожалуйста, введите путь ещё раз.")
if __name__ == "__main__":
    try:
        sf = g("Введите путь к папке с изображениями: ")
        tf = input("Введите название новой папки: ")
        if not o.path.isabs(tf): tf = o.path.join(sf, tf)
        p(sf, tf)
    except KeyboardInterrupt: print("\nПрограмма прервана пользователем.")
    except Exception as e: print(f"Ошибка: {e}")