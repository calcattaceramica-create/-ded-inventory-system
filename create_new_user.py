"""
إنشاء مستخدم جديد بصلاحيات
Create new user with permissions
"""
import sys
sys.path.insert(0, r'C:\Users\DELL\Desktop\DED_Portable_App')

from app import create_app, db
from app.models import User, Role

print("=" * 80)
print("👤 إنشاء مستخدم جديد")
print("👤 Create New User")
print("=" * 80)

# Get user input
print("\n📝 أدخل بيانات المستخدم الجديد:")
username = input("اسم المستخدم (Username): ").strip()
password = input("كلمة المرور (Password): ").strip()
email = input("البريد الإلكتروني (Email): ").strip()
full_name = input("الاسم الكامل (Full Name): ").strip()

# Ask for role
print("\n🎭 اختر الدور:")
print("1. admin - مدير (جميع الصلاحيات)")
print("2. user - مستخدم عادي (بدون صلاحيات)")
print("3. custom - دور مخصص")
role_choice = input("اختر (1/2/3): ").strip()

app = create_app()

with app.app_context():
    # Check if username exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"\n❌ اسم المستخدم '{username}' موجود مسبقاً!")
        sys.exit(1)
    
    # Check if email exists
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        print(f"\n❌ البريد الإلكتروني '{email}' موجود مسبقاً!")
        sys.exit(1)
    
    # Get role
    role = None
    is_admin = False
    
    if role_choice == '1':
        role = Role.query.filter_by(name='admin').first()
        is_admin = True
        print(f"\n✅ سيتم إنشاء المستخدم كمدير (Admin)")
    elif role_choice == '2':
        role = Role.query.filter_by(name='user').first()
        if not role:
            # Create user role
            role = Role(
                name='user',
                name_ar='مستخدم',
                description='Basic user role'
            )
            db.session.add(role)
            db.session.commit()
            print(f"\n✅ تم إنشاء دور 'user' جديد")
    else:
        # Show available roles
        roles = Role.query.all()
        print(f"\n📋 الأدوار المتاحة:")
        for i, r in enumerate(roles, 1):
            print(f"{i}. {r.name} ({r.name_ar}) - {len(r.permissions)} صلاحية")
        
        role_index = int(input("اختر رقم الدور: ").strip()) - 1
        role = roles[role_index]
    
    # Create user
    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        role_id=role.id if role else None,
        is_active=True,
        is_admin=is_admin
    )
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    print("\n" + "=" * 80)
    print("✅ تم إنشاء المستخدم بنجاح!")
    print("✅ User created successfully!")
    print("=" * 80)
    
    print(f"\n📋 بيانات المستخدم:")
    print(f"   - اسم المستخدم: {new_user.username}")
    print(f"   - كلمة المرور: {password}")
    print(f"   - البريد: {new_user.email}")
    print(f"   - الاسم الكامل: {new_user.full_name}")
    print(f"   - الدور: {role.name if role else 'بدون دور'}")
    print(f"   - مدير: {'نعم' if new_user.is_admin else 'لا'}")
    print(f"   - نشط: {'نعم' if new_user.is_active else 'لا'}")
    if role:
        print(f"   - عدد الصلاحيات: {len(role.permissions)}")
    
    print(f"\n🌐 يمكن الآن تسجيل الدخول:")
    print(f"   URL: http://127.0.0.1:5000/auth/login")
    print(f"   اسم المستخدم: {new_user.username}")
    print(f"   كلمة المرور: {password}")

