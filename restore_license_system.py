"""
استرجاع نظام التراخيص
Restore License System
"""
import shutil
import os

print("=" * 80)
print("🔄 استرجاع نظام التراخيص")
print("🔄 Restoring License System")
print("=" * 80)
print()

base_path = r"C:\Users\DELL\Desktop\DED_Portable_App"
backup_path = r"C:\Users\DELL\DED"

# Step 1: Restore auth/routes.py from backup
print("📝 الخطوة 1: استرجاع auth/routes.py...")
print()

auth_routes_backup = os.path.join(backup_path, "auth_routes_backup.py")
auth_routes_target = os.path.join(base_path, "app", "auth", "routes.py")

if os.path.exists(auth_routes_backup):
    try:
        shutil.copy(auth_routes_backup, auth_routes_target)
        print("   ✅ تم استرجاع auth/routes.py")
    except Exception as e:
        print(f"   ❌ خطأ في استرجاع auth/routes.py: {e}")
else:
    print("   ❌ ملف auth_routes_backup.py غير موجود")

print()

# Step 2: Restore login.html from backup
print("📝 الخطوة 2: استرجاع login.html...")
print()

login_backup = os.path.join(backup_path, "login.html")
login_target = os.path.join(base_path, "app", "templates", "auth", "login.html")

if os.path.exists(login_backup):
    try:
        shutil.copy(login_backup, login_target)
        print("   ✅ تم استرجاع login.html")
    except Exception as e:
        print(f"   ❌ خطأ في استرجاع login.html: {e}")
else:
    print("   ❌ ملف login.html backup غير موجود")

print()

# Step 3: Restore license_control.py
print("📝 الخطوة 3: استرجاع license_control.py...")
print()

# We need to recreate this file from the codebase
license_control_content = '''"""
License Control Module for DED Control Panel
وحدة التحكم في التراخيص لـ DED Control Panel
"""
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

class LicenseControl:
    """License Control Class"""
    
    def __init__(self, db_path=None):
        """Initialize with database path"""
        if db_path is None:
            self.db_path = Path(__file__).parent / 'licenses_master.db'
        else:
            self.db_path = Path(db_path)
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(str(self.db_path))
    
    def get_all_licenses(self):
        """Get all licenses with full details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(\'\'\'
            SELECT license_key, client_name, client_company, admin_username,
                   is_active, is_suspended, suspension_reason, expires_at, 
                   created_at, max_users, client_email, client_phone
            FROM licenses
            ORDER BY created_at DESC
        \'\'\')
        
        licenses = []
        for row in cursor.fetchall():
            licenses.append({
                'license_key': row[0],
                'client_name': row[1],
                'client_company': row[2],
                'admin_username': row[3],
                'is_active': bool(row[4]),
                'is_suspended': bool(row[5]),
                'suspension_reason': row[6],
                'expires_at': row[7],
                'created_at': row[8],
                'max_users': row[9],
                'client_email': row[10],
                'client_phone': row[11]
            })
        
        conn.close()
        return licenses
    
    def activate_license(self, license_key):
        """Activate a license"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(\'\'\'
                UPDATE licenses
                SET is_active = 1, is_suspended = 0, suspension_reason = NULL
                WHERE license_key = ?
            \'\'\', (license_key,))
            
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            
            return affected > 0, "تم تفعيل الترخيص بنجاح" if affected > 0 else "الترخيص غير موجود"
        except Exception as e:
            return False, f"خطأ: {str(e)}"
    
    def suspend_license(self, license_key, reason="تم الإيقاف من لوحة التحكم"):
        """Suspend a license"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(\'\'\'
                UPDATE licenses
                SET is_suspended = 1, suspension_reason = ?
                WHERE license_key = ?
            \'\'\', (reason, license_key))
            
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            
            return affected > 0, "تم إيقاف الترخيص بنجاح" if affected > 0 else "الترخيص غير موجود"
        except Exception as e:
            return False, f"خطأ: {str(e)}"
    
    def extend_license(self, license_key, days=30):
        """Extend license expiry date"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(\'\'\'
                UPDATE licenses
                SET expires_at = datetime(expires_at, '+' || ? || ' days')
                WHERE license_key = ?
            \'\'\', (days, license_key))
            
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            
            return affected > 0, f"تم تمديد الترخيص {days} يوم" if affected > 0 else "الترخيص غير موجود"
        except Exception as e:
            return False, f"خطأ: {str(e)}"
'''

license_control_path = os.path.join(base_path, "license_control.py")
try:
    with open(license_control_path, 'w', encoding='utf-8') as f:
        f.write(license_control_content)
    print("   ✅ تم إنشاء license_control.py")
except Exception as e:
    print(f"   ❌ خطأ في إنشاء license_control.py: {e}")

print()
print("=" * 80)
print("✅ تم استرجاع نظام التراخيص!")
print("=" * 80)
print()
print("📝 الخطوات التالية:")
print("   1. تحقق من الملفات المسترجعة")
print("   2. أعد تشغيل التطبيق")
print("   3. اختبر تسجيل الدخول مع license_key")
print()

