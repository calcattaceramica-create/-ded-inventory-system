"""
Add User ABDO to Database
إضافة المستخدم ABDO إلى قاعدة البيانات
"""
import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

# Database path
db_path = "C:/Users/DELL/Desktop/DED_Portable_App/tenant_C081D92695E08A84.db"

# User data
username = "ABDO"
email = "abdo@example.com"
password = "123456"  # كلمة المرور التي أدخلتها
full_name = "عبدو"
phone = ""
is_active = 1
is_admin = 0
language = "ar"

print("=" * 80)
print("🔧 إضافة المستخدم ABDO - Adding User ABDO")
print("=" * 80)
print()

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT id, username FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        print(f"⚠️  المستخدم {username} موجود بالفعل!")
        print(f"   ID: {existing_user[0]}")
        print()
        print("هل تريد تحديث كلمة المرور؟ (y/n)")
        # For now, just update the password
        password_hash = generate_password_hash(password)
        cursor.execute("""
            UPDATE users 
            SET password_hash = ?, email = ?, full_name = ?, is_active = ?
            WHERE username = ?
        """, (password_hash, email, full_name, is_active, username))
        conn.commit()
        print(f"✅ تم تحديث المستخدم {username} بنجاح!")
    else:
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Insert user
        cursor.execute("""
            INSERT INTO users 
            (username, email, password_hash, full_name, phone, is_active, 
             is_admin, language, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            email,
            password_hash,
            full_name,
            phone,
            is_active,
            is_admin,
            language,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        user_id = cursor.lastrowid
        
        print(f"✅ تم إضافة المستخدم بنجاح!")
        print(f"   ID: {user_id}")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   Full Name: {full_name}")
        print(f"   Active: {is_active}")
        print(f"   Admin: {is_admin}")
    
    # Verify user was added
    cursor.execute("SELECT id, username, email, is_active FROM users")
    all_users = cursor.fetchall()
    
    print()
    print("=" * 80)
    print("📋 جميع المستخدمين في قاعدة البيانات:")
    print("=" * 80)
    for user in all_users:
        print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Active: {user[3]}")
    
    conn.close()
    
    print()
    print("=" * 80)
    print("🎉 العملية اكتملت بنجاح!")
    print("=" * 80)
    print()
    print("الآن يمكنك تسجيل الدخول باستخدام:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   License Key: C081-D926-95E0-8A84")
    
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()

