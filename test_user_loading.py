"""
اختبار تحميل المستخدم
Test user loading
"""
import sys
sys.path.insert(0, r'C:\Users\DELL\Desktop\DED_Portable_App')

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"✅ Admin user found:")
        print(f"   - ID: {admin.id}")
        print(f"   - Username: {admin.username}")
        print(f"   - is_admin: {admin.is_admin}")
        print(f"   - role_id: {admin.role_id}")
        
        # Test has_permission method
        print(f"\n📋 Testing has_permission method:")
        print(f"   - has_permission('dashboard.view'): {admin.has_permission('dashboard.view')}")
        print(f"   - has_permission('inventory.stock.view'): {admin.has_permission('inventory.stock.view')}")
        print(f"   - has_permission('inventory.damaged.view'): {admin.has_permission('inventory.damaged.view')}")
        
        # Check role
        if admin.role:
            print(f"\n✅ Role found: {admin.role.name}")
            print(f"   - Role ID: {admin.role.id}")
            print(f"   - Permissions count: {len(admin.role.permissions)}")
            
            # Show first 5 permissions
            print(f"\n📋 First 5 permissions:")
            for i, perm in enumerate(admin.role.permissions[:5]):
                print(f"   {i+1}. {perm.name} ({perm.name_ar})")
        else:
            print(f"\n❌ No role assigned!")
    else:
        print("❌ Admin user NOT found!")

