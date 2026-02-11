"""
Create Desktop Shortcut for DED Application
"""
import os
from win32com.client import Dispatch

# Paths
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
app_path = r"C:\Users\DELL\Desktop\DED_Portable_App"
run_py = os.path.join(app_path, "run.py")
python_exe = r"C:\Python314\pythonw.exe"  # Using the Python from the error message
icon_path = os.path.join(app_path, "app", "static", "images", "logo.ico")  # If you have an icon

# Create shortcut
shortcut_path = os.path.join(desktop, "DED Application.lnk")

print("🔧 إنشاء اختصار على سطح المكتب...")
print()

try:
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = python_exe
    shortcut.Arguments = f'"{run_py}"'
    shortcut.WorkingDirectory = app_path
    shortcut.Description = "DED Dental Application"

    # Set icon if exists
    if os.path.exists(icon_path):
        shortcut.IconLocation = icon_path
    else:
        # Use default Python icon
        shortcut.IconLocation = python_exe

    shortcut.save()

    print("✅ تم إنشاء الاختصار على سطح المكتب بنجاح!")
    print(f"📍 المسار: {shortcut_path}")
    print()
    print("🎯 الآن يمكنك تشغيل التطبيق من سطح المكتب مباشرة!")
    print()
    print("📝 ملاحظة: انقر نقراً مزدوجاً على 'DED Application' على سطح المكتب")

except Exception as e:
    print(f"❌ خطأ: {e}")
    print()
    print("💡 يمكنك تشغيل التطبيق يدوياً من PowerShell:")
    print(f"   cd {app_path}")
    print("   python run.py")

