@echo off
chcp 65001 >nul
title 🎉 مدير التراخيص الفاخر المحمول - DED Portable License Manager

echo ================================================================================
echo 🎉 مدير التراخيص الفاخر المحمول - DED Portable License Manager
echo ================================================================================
echo.
echo 📍 الموقع: %~dp0
echo 📍 Location: %~dp0
echo.

REM Get the current directory (where this batch file is located)
set "APP_DIR=%~dp0DED_License_Manager"

REM Check if the folder exists
if not exist "%APP_DIR%" (
    echo ❌ خطأ: مجلد التطبيق غير موجود!
    echo ❌ Error: Application folder not found!
    echo.
    echo 📁 المتوقع: %APP_DIR%
    echo 📁 Expected: %APP_DIR%
    echo.
    pause
    exit /b 1
)

echo ✅ تم العثور على مجلد التطبيق
echo ✅ Application folder found
echo.

REM Change to the application directory
cd /d "%APP_DIR%"

echo 📂 المجلد الحالي: %CD%
echo 📂 Current directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت على هذا الجهاز!
    echo ❌ Error: Python is not installed on this computer!
    echo.
    echo 💡 الرجاء تثبيت Python من: https://www.python.org/downloads/
    echo 💡 Please install Python from: https://www.python.org/downloads/
    echo.
    echo 📝 ملاحظة: يجب تثبيت Python على كل جهاز تريد استخدام التطبيق عليه
    echo 📝 Note: Python must be installed on each computer you want to use the app on
    echo.
    pause
    exit /b 1
)

echo ✅ Python مثبت
echo ✅ Python is installed
python --version
echo.

REM Check if required packages are installed
echo 📦 التحقق من المكتبات المطلوبة...
echo 📦 Checking required packages...
echo.

pip show werkzeug >nul 2>&1
if errorlevel 1 (
    echo ⚠️ تثبيت المكتبات المطلوبة...
    echo ⚠️ Installing required packages...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ فشل تثبيت المكتبات!
        echo ❌ Failed to install packages!
        echo.
        echo 💡 تأكد من اتصالك بالإنترنت
        echo 💡 Make sure you are connected to the internet
        echo.
        pause
        exit /b 1
    )
)

echo ✅ جميع المكتبات جاهزة!
echo ✅ All packages ready!
echo.

REM Check if the main application file exists
if not exist "DED_Control_Panel.pyw" (
    echo ❌ خطأ: ملف التطبيق الرئيسي غير موجود!
    echo ❌ Error: Main application file not found!
    echo.
    echo 📁 المتوقع: %CD%\DED_Control_Panel.pyw
    echo 📁 Expected: %CD%\DED_Control_Panel.pyw
    echo.
    pause
    exit /b 1
)

echo 🎯 تشغيل لوحة التحكم...
echo 🎯 Launching Control Panel...
echo.

REM Start the Control Panel
start pythonw DED_Control_Panel.pyw

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ أثناء التشغيل!
    echo ❌ An error occurred!
    echo.
    echo 💡 جرب التشغيل اليدوي:
    echo 💡 Try manual start:
    echo    python DED_Control_Panel.pyw
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ تم التشغيل بنجاح!
echo ✅ Started successfully!
echo.
echo 💡 إذا لم تظهر النافذة، تحقق من شريط المهام
echo 💡 If the window doesn't appear, check the taskbar
echo.
echo 📝 ملاحظة: يمكنك إغلاق هذه النافذة الآن
echo 📝 Note: You can close this window now
echo.
timeout /t 5

