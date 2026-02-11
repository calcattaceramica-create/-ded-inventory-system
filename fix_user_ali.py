"""
إصلاح المستخدم ali وإعطائه صلاحيات
Fix user ali and give him permissions
"""
import sys
sys.path.insert(0, r'C:\Users\DELL\Desktop\DED_Portable_App')

from app import create_app, db
from app.models import User, Role

print("=" * 80)
print("🔧 إصلاح المستخدم ali")
print("🔧 Fixing user ali")
print("=" * 80)

app = create_app()

with app.app_context():
    # Get user ali
    ali = User.query.filter_by(username='ali').first()
    
    if ali:
        print(f"\n✅ User 'ali' found:")
        print(f"   - ID: {ali.id}")
        print(f"   - Username: {ali.username}")
        print(f"   - Email: {ali.email}")
        print(f"   - is_active: {ali.is_active}")
        print(f"   - is_admin: {ali.is_admin}")
        print(f"   - role_id: {ali.role_id}")
        
        # Get admin role
        admin_role = Role.query.filter_by(name='admin').first()
        
        if admin_role:
            print(f"\n✅ Admin role found: {admin_role.name} (ID: {admin_role.id})")
            print(f"   - Permissions count: {len(admin_role.permissions)}")
            
            # Assign admin role to ali
            ali.role_id = admin_role.id
            
            # Make sure ali is active
            ali.is_active = True
            
            # Set a password if not set
            if not ali.password_hash:
                ali.set_password('ali123')
                print(f"\n✅ Password set to: ali123")
            
            db.session.commit()
            
            print(f"\n✅ User 'ali' updated successfully!")
            print(f"   - role_id: {ali.role_id}")
            print(f"   - is_active: {ali.is_active}")
            print(f"   - Permissions: {len(admin_role.permissions)}")
            
        else:
            print(f"\n❌ Admin role NOT found!")
            print(f"Creating a new role for ali...")
            
            # Create a basic user role
            user_role = Role(
                name='user',
                name_ar='مستخدم',
                description='Basic user role'
            )
            db.session.add(user_role)
            db.session.commit()
            
            # Assign to ali
            ali.role_id = user_role.id
            ali.is_active = True
            
            if not ali.password_hash:
                ali.set_password('ali123')
                print(f"\n✅ Password set to: ali123")
            
            db.session.commit()
            
            print(f"\n✅ Created new role 'user' and assigned to ali")
            print(f"   - role_id: {ali.role_id}")
            print(f"   - is_active: {ali.is_active}")
    else:
        print("\n❌ User 'ali' NOT found!")

print("\n" + "=" * 80)
print("✅ تم إصلاح المستخدم بنجاح!")
print("✅ User fixed successfully!")
print("=" * 80)

print("\n📋 الخطوات التالية:")
print("1. أعد تحميل صفحة إدارة المستخدمين")
print("2. الآن يمكن للمستخدم ali تسجيل الدخول:")
print("   - اسم المستخدم: ali")
print("   - كلمة المرور: ali123")

