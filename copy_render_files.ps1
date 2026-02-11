# نسخ ملفات Render إلى مجلد التطبيق
# Copy Render deployment files to application directory

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "📦 نسخ ملفات Render إلى مجلد التطبيق" -ForegroundColor Yellow
Write-Host "📦 Copying Render files to application directory" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# المسارات
$sourceDir = "C:\Users\DELL\DED"
$destDir = "C:\Users\DELL\Desktop\DED_Portable_App"

# الملفات المطلوبة
$files = @(
    "render.yaml",
    "Procfile",
    "runtime.txt",
    "init_db.py"
)

# التحقق من وجود المجلد الهدف
if (-not (Test-Path $destDir)) {
    Write-Host "❌ خطأ: مجلد التطبيق غير موجود!" -ForegroundColor Red
    Write-Host "❌ Error: Application directory not found!" -ForegroundColor Red
    Write-Host "   المسار: $destDir" -ForegroundColor Gray
    Write-Host ""
    pause
    exit 1
}

Write-Host "✅ تم العثور على مجلد التطبيق" -ForegroundColor Green
Write-Host "   المسار: $destDir" -ForegroundColor Gray
Write-Host ""

# نسخ الملفات
$successCount = 0
$failCount = 0

foreach ($file in $files) {
    $sourcePath = Join-Path $sourceDir $file
    $destPath = Join-Path $destDir $file
    
    Write-Host "📄 نسخ: $file" -ForegroundColor Cyan
    
    if (Test-Path $sourcePath) {
        try {
            Copy-Item $sourcePath -Destination $destPath -Force
            Write-Host "   ✅ تم النسخ بنجاح" -ForegroundColor Green
            $successCount++
        }
        catch {
            Write-Host "   ❌ فشل النسخ: $_" -ForegroundColor Red
            $failCount++
        }
    }
    else {
        Write-Host "   ❌ الملف غير موجود في المصدر!" -ForegroundColor Red
        $failCount++
    }
    Write-Host ""
}

# النتيجة النهائية
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "📊 النتيجة:" -ForegroundColor Yellow
Write-Host "   ✅ نجح: $successCount ملف" -ForegroundColor Green
Write-Host "   ❌ فشل: $failCount ملف" -ForegroundColor Red
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

if ($successCount -eq $files.Count) {
    Write-Host "🎉 تم نسخ جميع الملفات بنجاح!" -ForegroundColor Green
    Write-Host "🎉 All files copied successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 الخطوة التالية:" -ForegroundColor Yellow
    Write-Host "   1. افتح PowerShell في مجلد التطبيق" -ForegroundColor White
    Write-Host "   2. شغّل الأوامر التالية:" -ForegroundColor White
    Write-Host ""
    Write-Host "      cd C:\Users\DELL\Desktop\DED_Portable_App" -ForegroundColor Cyan
    Write-Host "      git add render.yaml Procfile runtime.txt init_db.py" -ForegroundColor Cyan
    Write-Host "      git commit -m `"Add Render deployment configuration`"" -ForegroundColor Cyan
    Write-Host "      git push origin main" -ForegroundColor Cyan
    Write-Host ""
}
else {
    Write-Host "⚠️ بعض الملفات لم يتم نسخها!" -ForegroundColor Yellow
    Write-Host "⚠️ Some files were not copied!" -ForegroundColor Yellow
}

Write-Host ""
pause

