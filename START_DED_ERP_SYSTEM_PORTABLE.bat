@echo off
chcp 65001 >nul
title DED ERP System - Portable Launcher

echo ================================================================================
echo.
echo    🚀 DED ERP System - Portable Launcher
echo    نظام DED ERP - مشغل محمول
echo.
echo ================================================================================
echo.

REM Get the drive letter where this batch file is located
set "USB_DRIVE=%~d0"
set "APP_PATH=%USB_DRIVE%\"

echo 📍 الموقع: %APP_PATH%
echo 📍 Location: %APP_PATH%
echo.

REM Check if Python is installed
echo 🔍 التحقق من وجود Python...
echo 🔍 Checking for Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ خطأ: Python غير مثبت على هذا الجهاز!
    echo ❌ Error: Python is not installed on this computer!
    echo.
    echo 💡 يرجى تثبيت Python 3.7 أو أحدث من:
    echo 💡 Please install Python 3.7 or newer from:
    echo    https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ تم العثور على Python
echo.

REM Change to app directory
cd /d "%APP_PATH%"

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ⚠️ تحذير: ملف requirements.txt غير موجود
    echo ⚠️ Warning: requirements.txt not found
    echo.
)

REM Install/check required packages
echo 📦 التحقق من المكتبات المطلوبة...
echo 📦 Checking required packages...
echo.

pip install -q -r requirements.txt 2>nul
if errorlevel 1 (
    echo ⚠️ تحذير: بعض المكتبات قد لا تكون مثبتة بشكل صحيح
    echo ⚠️ Warning: Some packages may not be installed correctly
    echo.
)

echo ✅ المكتبات جاهزة
echo.

REM Start the Flask application
echo ================================================================================
echo.
echo    🎯 بدء تشغيل نظام DED ERP...
echo    🎯 Starting DED ERP System...
echo.
echo ================================================================================
echo.
echo 🌐 سيتم فتح المتصفح تلقائياً على:
echo 🌐 Browser will open automatically at:
echo    http://127.0.0.1:5000
echo.
echo 💡 لإيقاف التطبيق، اضغط Ctrl+C في هذه النافذة
echo 💡 To stop the application, press Ctrl+C in this window
echo.
echo ================================================================================
echo.

REM Start Flask app
python run.py

REM If Flask exits, pause to show any error messages
echo.
echo ================================================================================
echo.
echo ⚠️ تم إيقاف التطبيق
echo ⚠️ Application stopped
echo.
pause

