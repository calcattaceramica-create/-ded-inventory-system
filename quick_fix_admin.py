"""
Quick fix: Make admin user is_admin=True
إصلاح سريع: جعل المستخدم admin مدير نظام
"""
import os
os.environ['FLASK_ENV'] = 'production'

from run import app, db
from app.models import User

print("=" * 80)
print("🔧 إصلاح سريع للمستخدم admin")
print("🔧 Quick fix for admin user")
print("=" * 80)

with app.app_context():
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        print("\n❌ المستخدم admin غير موجود!")
        print("❌ Admin user not found!")
        print("\n🔧 سيتم إنشاء مستخدم admin جديد...")
        
        admin = User(
            username='admin',
            email='admin@example.com',
            full_name='مدير النظام',
            is_active=True,
            is_admin=True,
            language='ar',
            branch_id=1,
            role_id=1
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ تم إنشاء المستخدم admin")
        print("✅ Admin user created")
    else:
        print(f"\n👤 المستخدم admin موجود:")
        print(f"   - ID: {admin.id}")
        print(f"   - Username: {admin.username}")
        print(f"   - is_admin: {admin.is_admin}")
        print(f"   - is_active: {admin.is_active}")
        print(f"   - role_id: {admin.role_id}")
        
        if not admin.is_admin:
            print("\n⚠️ المستخدم admin ليس is_admin=True")
            print("⚠️ Admin user is not is_admin=True")
            print("🔧 سيتم تفعيل is_admin...")
            
            admin.is_admin = True
            admin.is_active = True
            db.session.commit()
            
            print("✅ تم تفعيل is_admin")
            print("✅ is_admin activated")
        else:
            print("\n✅ المستخدم admin صحيح (is_admin=True)")
            print("✅ Admin user is correct (is_admin=True)")
    
    # Test permission
    print(f"\n🔍 اختبار الصلاحيات:")
    print(f"   - has_permission('dashboard.view'): {admin.has_permission('dashboard.view')}")
    print(f"   - has_permission('settings.roles.view'): {admin.has_permission('settings.roles.view')}")
    print(f"   - has_permission('settings.view'): {admin.has_permission('settings.view')}")

print("\n" + "=" * 80)
print("✅ تم الانتهاء!")
print("✅ Done!")
print("\n📝 الآن:")
print("   1. سجل خروج من التطبيق")
print("   2. سجل دخول مرة أخرى بـ admin/admin123")
print("   3. يجب أن تعمل جميع الصفحات!")
print("\n📝 Now:")
print("   1. Logout from the app")
print("   2. Login again with admin/admin123")
print("   3. All pages should work!")
print("=" * 80)

