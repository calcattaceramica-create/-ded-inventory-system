"""
Fix Tenant Middleware - Disable Multi-Tenancy
إصلاح Middleware - تعطيل نظام التراخيص المتعددة
"""

import os
import shutil
from pathlib import Path

def fix_tenant_middleware():
    """Disable tenant middleware by modifying __init__.py"""
    
    app_init_path = Path("C:/Users/DELL/Desktop/DED_Portable_App/app/__init__.py")
    
    print("=" * 70)
    print("🔧 Fixing Tenant Middleware")
    print("=" * 70)
    
    try:
        # Read the file
        with open(app_init_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Backup the original file
        backup_path = app_init_path.with_suffix('.py.backup')
        shutil.copy2(app_init_path, backup_path)
        print(f"\n✅ Backup created: {backup_path}")
        
        # Comment out the tenant middleware initialization
        old_code = """    # Initialize Multi-Tenancy middleware
    from app.tenant_middleware import init_tenant_middleware
    init_tenant_middleware(app)"""
        
        new_code = """    # Initialize Multi-Tenancy middleware - DISABLED (No license system)
    # from app.tenant_middleware import init_tenant_middleware
    # init_tenant_middleware(app)"""
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            print(f"\n✅ Tenant middleware disabled!")
        else:
            print(f"\n⚠️  Tenant middleware code not found or already disabled")
        
        # Write the modified content
        with open(app_init_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ File updated: {app_init_path}")
        
        print("\n" + "=" * 70)
        print("✅ Tenant middleware fixed successfully!")
        print("=" * 70)
        print("\n📝 Next steps:")
        print("   1. أعد تشغيل التطبيق (Ctrl+C ثم python run.py)")
        print("   2. سجل الدخول مرة أخرى")
        print("\n" + "=" * 70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_tenant_middleware()

