"""
Fix base.html - Replace auth.change_language with settings.change_language
"""
import os

base_html_path = r"C:\Users\DELL\Desktop\DED_Portable_App\app\templates\base.html"

print("🔧 Fixing base.html...")
print()

try:
    # Read the file
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace auth.change_language with settings.change_language
    original_content = content
    content = content.replace("url_for('auth.change_language'", "url_for('settings.change_language'")
    
    # Write back
    with open(base_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ تم التعديل بنجاح!")
        print("✅ تم استبدال auth.change_language بـ settings.change_language")
    else:
        print("⚠️ لم يتم العثور على auth.change_language")
    
except Exception as e:
    print(f"❌ خطأ: {e}")

print()
print("🎯 الآن أعد تشغيل التطبيق!")

