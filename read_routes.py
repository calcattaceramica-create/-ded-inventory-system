with open(r'C:\Users\DELL\Desktop\DED_Portable_App\app\main\routes.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i in range(23, 40):
        print(f"{i+1}: {lines[i]}", end='')

