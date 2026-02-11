"""
إزالة نظام التراخيص من التطبيق
Remove License System from Application
"""
import os
import shutil

print("=" * 80)
print("🗑️ إزالة نظام التراخيص من التطبيق")
print("🗑️ Removing License System from Application")
print("=" * 80)
print()

# المسار الأساسي
base_path = r"C:\Users\DELL\Desktop\DED_Portable_App"

# الملفات المطلوب حذفها
files_to_remove = [
    "license_control.py",
    "licenses.json",
    "licenses_master.db",
    "DED_Control_Panel.pyw",
    "activate_license.py",
    "license_manager_simple.py",
    "multi_tenant_login_backup.py",
    "auto_login.html",
]

# المجلدات المطلوب حذفها
folders_to_remove = [
    "tenant_databases",
]

# حذف الملفات
print("📄 حذف الملفات المتعلقة بالتراخيص...")
print("📄 Removing license-related files...")
print()

removed_files = 0
for file in files_to_remove:
    file_path = os.path.join(base_path, file)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"   ✅ تم حذف: {file}")
            removed_files += 1
        except Exception as e:
            print(f"   ❌ فشل حذف {file}: {e}")
    else:
        print(f"   ⚠️ غير موجود: {file}")

print()

# حذف المجلدات
print("📁 حذف المجلدات المتعلقة بالتراخيص...")
print("📁 Removing license-related folders...")
print()

removed_folders = 0
for folder in folders_to_remove:
    folder_path = os.path.join(base_path, folder)
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"   ✅ تم حذف: {folder}")
            removed_folders += 1
        except Exception as e:
            print(f"   ❌ فشل حذف {folder}: {e}")
    else:
        print(f"   ⚠️ غير موجود: {folder}")

print()
print("=" * 80)
print(f"📊 النتيجة:")
print(f"   ✅ تم حذف {removed_files} ملف")
print(f"   ✅ تم حذف {removed_folders} مجلد")
print("=" * 80)
print()

print("⚠️ ملاحظة: يجب تعديل الملفات التالية يدوياً:")
print("⚠️ Note: The following files need manual editing:")
print()
print("   1. app/auth/routes.py - إزالة license_key من نموذج تسجيل الدخول")
print("   2. app/templates/auth/login.html - إزالة حقل license_key")
print("   3. app/models.py - إزالة دوال has_valid_license و get_license_status")
print()
print("✅ تم!")

