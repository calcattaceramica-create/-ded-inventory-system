"""
إعادة تعيين كلمة مرور المدير
Reset admin password
"""
import sys
sys.path.insert(0, r'C:\Users\DELL\Desktop\DED_Portable_App')

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

print("=" * 80)
print("🔧 إعادة تعيين كلمة مرور المدير")
print("🔧 Resetting admin password")
print("=" * 80)

app = create_app()

with app.app_context():
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"\n✅ Admin user found: {admin.username}")
        print(f"   - ID: {admin.id}")
        print(f"   - is_admin: {admin.is_admin}")
        print(f"   - role_id: {admin.role_id}")
        
        # Reset password
        new_password = 'admin123'
        admin.password_hash = generate_password_hash(new_password)
        
        # Make sure is_admin is True
        admin.is_admin = True
        
        # Make sure is_active is True
        admin.is_active = True
        
        # Reset failed login attempts
        admin.failed_login_attempts = 0
        admin.account_locked_until = None
        
        db.session.commit()
        
        print(f"\n✅ Password reset successfully!")
        print(f"   - New password: {new_password}")
        print(f"   - is_admin: {admin.is_admin}")
        print(f"   - is_active: {admin.is_active}")
        
    else:
        print("\n❌ Admin user NOT found!")

print("\n" + "=" * 80)
print("✅ تم إعادة تعيين كلمة المرور بنجاح!")
print("✅ Password reset successfully!")
print("=" * 80)

print("\n📋 الخطوات التالية:")
print("1. امسح الكوكيز في المتصفح (Ctrl + Shift + Delete)")
print("2. اذهب إلى: http://127.0.0.1:5000/auth/login")
print("3. سجل الدخول:")
print("   - اسم المستخدم: admin")
print("   - كلمة المرور: admin123")

