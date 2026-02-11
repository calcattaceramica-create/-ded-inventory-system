# Create Desktop Shortcut for DED Application

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "DED Application.lnk"
$TargetPath = "C:\Users\DELL\Desktop\DED_Portable_App\Start_DED_App.bat"
$WorkingDirectory = "C:\Users\DELL\Desktop\DED_Portable_App"

Write-Host "Creating desktop shortcut..." -ForegroundColor Cyan
Write-Host ""

try {
    # Remove old shortcut if exists
    if (Test-Path $ShortcutPath) {
        Remove-Item $ShortcutPath -Force
        Write-Host "Removed old shortcut" -ForegroundColor Yellow
    }

    $WScriptShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetPath
    $Shortcut.WorkingDirectory = $WorkingDirectory
    $Shortcut.Description = "DED Dental Application"
    $Shortcut.Save()

    Write-Host "SUCCESS: Desktop shortcut created!" -ForegroundColor Green
    Write-Host "Path: $ShortcutPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Double-click 'DED Application' on desktop to start!" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "You can run the app manually:" -ForegroundColor Yellow
    Write-Host "   cd C:\Users\DELL\Desktop\DED_Portable_App" -ForegroundColor White
    Write-Host "   python run.py" -ForegroundColor White
}

