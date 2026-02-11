"""
إضافة صلاحيات المخزون التالف للمستخدم admin
Add damaged inventory permissions to admin user
"""
import sqlite3
import os

print("=" * 80)
print("🔧 إضافة صلاحيات المخزون التالف")
print("🔧 Adding damaged inventory permissions")
print("=" * 80)

# Database path
db_path = r"C:\Users\DELL\Desktop\DED_Portable_App\erp_system.db"

if not os.path.exists(db_path):
    print(f"\n❌ قاعدة البيانات غير موجودة: {db_path}")
    exit(1)

print(f"\n📂 قاعدة البيانات: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if admin user exists
    cursor.execute("SELECT id, username, is_admin FROM users WHERE username = 'admin'")
    admin_user = cursor.fetchone()
    
    if admin_user:
        print(f"\n✅ المستخدم admin موجود:")
        print(f"   - ID: {admin_user[0]}")
        print(f"   - Username: {admin_user[1]}")
        print(f"   - Is Admin: {admin_user[2]}")
        
        # Update admin user to be admin
        if not admin_user[2]:
            print("\n🔄 تحديث المستخدم admin ليكون مدير...")
            cursor.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
            conn.commit()
            print("✅ تم تحديث المستخدم admin")
        else:
            print("\n✅ المستخدم admin هو مدير بالفعل")
    else:
        print("\n❌ المستخدم admin غير موجود!")
        print("سأقوم بإنشائه...")
        
        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash('admin123')
        
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name, is_admin, is_active, language)
            VALUES ('admin', 'admin@example.com', ?, 'Administrator', 1, 1, 'ar')
        """, (password_hash,))
        conn.commit()
        print("✅ تم إنشاء المستخدم admin")
    
    # Check permissions table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='permissions'")
    if cursor.fetchone():
        print("\n📋 التحقق من الصلاحيات...")
        
        # Add damaged inventory permissions if they don't exist
        permissions_to_add = [
            ('inventory.damaged.view', 'عرض المخزون التالف', 'inventory'),
            ('inventory.damaged.add', 'إضافة مخزون تالف', 'inventory'),
            ('inventory.damaged.edit', 'تعديل مخزون تالف', 'inventory'),
            ('inventory.damaged.delete', 'حذف مخزون تالف', 'inventory'),
        ]
        
        for perm_name, perm_name_ar, module in permissions_to_add:
            cursor.execute("SELECT id FROM permissions WHERE name = ?", (perm_name,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO permissions (name, name_ar, module)
                    VALUES (?, ?, ?)
                """, (perm_name, perm_name_ar, module))
                print(f"   ✅ تم إضافة صلاحية: {perm_name_ar}")
            else:
                print(f"   ℹ️  الصلاحية موجودة: {perm_name_ar}")
        
        conn.commit()
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ تم إصلاح صلاحيات المستخدم admin بنجاح!")
    print("✅ Admin permissions fixed successfully!")
    print("=" * 80)
    
    print("\n📋 الخطوات التالية:")
    print("1. سجل الخروج من التطبيق")
    print("2. سجل الدخول مرة أخرى بحساب admin")
    print("3. جرب الدخول إلى صفحة المخزون التالف")
    print("4. URL: http://127.0.0.1:5000/inventory/damaged-inventory")
    
except Exception as e:
    print(f"\n❌ خطأ: {str(e)}")
    import traceback
    traceback.print_exc()

