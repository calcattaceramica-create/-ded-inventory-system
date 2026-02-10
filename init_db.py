"""
Initialize database for production deployment
تهيئة قاعدة البيانات للنشر الإنتاجي
"""
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Role, Permission, Branch

print("=" * 80)
print("🔧 تهيئة قاعدة البيانات")
print("🔧 Initializing Database")
print("=" * 80)

app = create_app()

with app.app_context():
    # Create all tables
    print("\n📝 إنشاء الجداول...")
    print("📝 Creating tables...")
    db.create_all()
    print("✅ تم إنشاء الجداول بنجاح")
    print("✅ Tables created successfully")
    
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        print("\n👤 إنشاء مستخدم admin...")
        print("👤 Creating admin user...")
        
        # Create admin role
        admin_role = Role(
            name='admin',
            name_ar='مدير النظام',
            description='System Administrator',
            description_en='System Administrator'
        )
        db.session.add(admin_role)
        db.session.commit()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@ded-erp.com',
            full_name='System Administrator',
            is_active=True,
            is_admin=True,
            role_id=admin_role.id
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        print("✅ تم إنشاء مستخدم admin")
        print("✅ Admin user created")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   ⚠️  غيّر كلمة المرور فوراً!")
        print(f"   ⚠️  Change password immediately!")
    else:
        print("\n✅ مستخدم admin موجود بالفعل")
        print("✅ Admin user already exists")
    
    # Create default branch if not exists
    branch = Branch.query.filter_by(name='Main Branch').first()
    if not branch:
        print("\n🏢 إنشاء الفرع الرئيسي...")
        print("🏢 Creating main branch...")
        
        branch = Branch(
            name='Main Branch',
            name_ar='الفرع الرئيسي',
            code='MAIN',
            is_active=True
        )
        db.session.add(branch)
        db.session.commit()
        
        print("✅ تم إنشاء الفرع الرئيسي")
        print("✅ Main branch created")
    else:
        print("\n✅ الفرع الرئيسي موجود بالفعل")
        print("✅ Main branch already exists")

print("\n" + "=" * 80)
print("✅ تم تهيئة قاعدة البيانات بنجاح!")
print("✅ Database initialized successfully!")
print("=" * 80)

