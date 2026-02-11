"""
Test Login for User ABDO
اختبار تسجيل الدخول للمستخدم ABDO
"""
import sqlite3
from werkzeug.security import check_password_hash

# Database path
db_path = "C:/Users/DELL/Desktop/DED_Portable_App/tenant_C081D92695E08A84.db"

# Test credentials
username = "ABDO"
password = "123456"

print("=" * 80)
print("🔍 اختبار تسجيل الدخول - Testing Login")
print("=" * 80)
print()

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Find user
    cursor.execute("""
        SELECT id, username, email, password_hash, is_active, is_admin
        FROM users 
        WHERE username = ?
    """, (username,))
    
    user = cursor.fetchone()
    
    if not user:
        print(f"❌ المستخدم '{username}' غير موجود في قاعدة البيانات!")
        print()
        print("المستخدمون الموجودون:")
        cursor.execute("SELECT id, username FROM users")
        all_users = cursor.fetchall()
        for u in all_users:
            print(f"  - ID: {u[0]}, Username: {u[1]}")
    else:
        user_id, db_username, email, password_hash, is_active, is_admin = user
        
        print(f"✅ المستخدم موجود!")
        print(f"   ID: {user_id}")
        print(f"   Username: {db_username}")
        print(f"   Email: {email}")
        print(f"   Active: {is_active}")
        print(f"   Admin: {is_admin}")
        print()
        
        # Test password
        print(f"🔑 اختبار كلمة المرور...")
        if check_password_hash(password_hash, password):
            print(f"✅ كلمة المرور صحيحة!")
        else:
            print(f"❌ كلمة المرور خاطئة!")
            print(f"   Password Hash: {password_hash[:50]}...")
        
        print()
        
        # Check if active
        if is_active:
            print(f"✅ الحساب نشط")
        else:
            print(f"❌ الحساب غير نشط!")
    
    conn.close()
    
    print()
    print("=" * 80)
    print("📋 معلومات قاعدة البيانات:")
    print("=" * 80)
    print(f"Database: {db_path}")
    print(f"License Key: C081-D926-95E0-8A84")
    print()
    
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()

