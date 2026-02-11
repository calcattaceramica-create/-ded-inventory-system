@echo off
chcp 65001 >nul
title 🎉 مدير التراخيص الفاخر - DED License Manager

echo ================================================================================
echo 🎉 مدير التراخيص الفاخر - DED License Manager
echo ================================================================================
echo.
echo 🚀 جاري تشغيل لوحة التحكم...
echo 🚀 Starting Control Panel...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت!
    echo ❌ Error: Python is not installed!
    echo.
    echo 💡 الرجاء تثبيت Python من: https://www.python.org/downloads/
    echo 💡 Please install Python from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Start the Control Panel
start pythonw DED_Control_Panel.pyw

echo.
echo ✅ تم تشغيل لوحة التحكم بنجاح!
echo ✅ Control Panel started successfully!
echo.
echo 💡 إذا لم تظهر النافذة، شغّل الأمر التالي:
echo 💡 If the window doesn't appear, run:
echo    python DED_Control_Panel.pyw
echo.
pause

