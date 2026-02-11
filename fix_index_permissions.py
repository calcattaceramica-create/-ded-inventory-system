"""
إصلاح صلاحيات الصفحة الرئيسية
Fix index page permissions
"""
import sqlite3
import os

print("=" * 80)
print("🔧 إصلاح صلاحيات الصفحة الرئيسية")
print("🔧 Fixing index page permissions")
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
    
    # Check admin user
    cursor.execute("SELECT id, username, is_admin, role_id FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    if admin:
        print(f"\n✅ المستخدم admin:")
        print(f"   - ID: {admin[0]}")
        print(f"   - Username: {admin[1]}")
        print(f"   - Is Admin: {admin[2]}")
        print(f"   - Role ID: {admin[3]}")
        
        # Make sure admin is admin
        if not admin[2]:
            cursor.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
            conn.commit()
            print("\n✅ تم تحديث المستخدم admin ليكون مدير")
    
    # Add all necessary permissions
    permissions_to_add = [
        ('dashboard.view', 'عرض لوحة التحكم', 'main'),
        ('inventory.view', 'عرض المخزون', 'inventory'),
        ('inventory.stock.view', 'عرض المخزون', 'inventory'),
        ('inventory.products.view', 'عرض المنتجات', 'inventory'),
        ('inventory.damaged.view', 'عرض المخزون التالف', 'inventory'),
        ('sales.view', 'عرض المبيعات', 'sales'),
        ('purchases.view', 'عرض المشتريات', 'purchases'),
    ]
    
    print("\n📋 إضافة الصلاحيات...")
    for perm_name, perm_name_ar, module in permissions_to_add:
        cursor.execute("SELECT id FROM permissions WHERE name = ?", (perm_name,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO permissions (name, name_ar, module)
                VALUES (?, ?, ?)
            """, (perm_name, perm_name_ar, module))
            print(f"   ✅ تم إضافة: {perm_name_ar}")
        else:
            print(f"   ℹ️  موجودة: {perm_name_ar}")
    
    conn.commit()
    
    # Get admin role
    if admin and admin[3]:
        role_id = admin[3]
        print(f"\n📋 إضافة الصلاحيات للدور (Role ID: {role_id})...")
        
        # Get all permissions
        cursor.execute("SELECT id, name FROM permissions")
        all_perms = cursor.fetchall()
        
        for perm_id, perm_name in all_perms:
            # Check if role already has this permission
            cursor.execute("""
                SELECT id FROM role_permissions 
                WHERE role_id = ? AND permission_id = ?
            """, (role_id, perm_id))
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO role_permissions (role_id, permission_id)
                    VALUES (?, ?)
                """, (role_id, perm_id))
                print(f"   ✅ تم ربط: {perm_name}")
        
        conn.commit()
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ تم إصلاح الصلاحيات بنجاح!")
    print("✅ Permissions fixed successfully!")
    print("=" * 80)
    
    print("\n📋 الخطوات التالية:")
    print("1. أعد تحميل الصفحة في المتصفح (F5)")
    print("2. إذا لم يعمل، امسح الكوكيز وسجل الدخول مرة أخرى")
    print("3. اذهب إلى: http://127.0.0.1:5000/auth/login")
    
except Exception as e:
    print(f"\n❌ خطأ: {str(e)}")
    import traceback
    traceback.print_exc()

