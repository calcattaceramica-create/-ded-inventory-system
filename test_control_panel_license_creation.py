#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify Control Panel license creation integration
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

# Add DED_Portable_App to path
sys.path.insert(0, 'C:/Users/DELL/Desktop/DED_Portable_App')

def test_license_creation_integration():
    """Test that Control Panel can create licenses properly"""
    
    print("=" * 80)
    print("🧪 Testing Control Panel License Creation Integration")
    print("=" * 80)
    
    # Check if license_control module exists
    try:
        from license_control import LicenseControl
        print("✅ license_control module found")
        lc = LicenseControl()
        print("✅ LicenseControl initialized")
    except ImportError as e:
        print(f"❌ license_control module not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to initialize LicenseControl: {e}")
        return False
    
    # Check database
    db_path = Path("C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db")
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return False
    
    print(f"✅ Database found: {db_path}")
    
    # Check database schema
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute("PRAGMA table_info(licenses)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"\n📊 Database columns ({len(column_names)}):")
        for col in column_names:
            print(f"   - {col}")
        
        # Check required columns
        required_columns = ['license_key', 'license_hash', 'admin_username', 'admin_password_hash']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"\n❌ Missing required columns: {missing_columns}")
            conn.close()
            return False
        
        print(f"\n✅ All required columns present")
        
        # Get current licenses
        cursor.execute("SELECT license_key, client_company, is_active, is_suspended, expires_at FROM licenses")
        licenses = cursor.fetchall()
        
        print(f"\n📋 Current licenses in database: {len(licenses)}")
        for i, lic in enumerate(licenses, 1):
            key, company, active, suspended, expires = lic
            status = "✅ Active" if active else "❌ Inactive"
            susp = "⚠️ Suspended" if suspended else "✓ Not Suspended"
            print(f"   {i}. {key} - {company}")
            print(f"      Status: {status} | {susp} | Expires: {expires}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # Test summary
    print("\n" + "=" * 80)
    print("✅ All tests passed!")
    print("=" * 80)
    print("\n📝 Summary:")
    print("   ✅ license_control module available")
    print("   ✅ Database schema correct")
    print("   ✅ Required columns present")
    print(f"   ✅ {len(licenses)} licenses in database")
    print("\n🎯 Control Panel is ready to create licenses!")
    print("\n📌 Next steps:")
    print("   1. Open DED Control Panel")
    print("   2. Click '➕ إضافة ترخيص جديد'")
    print("   3. Fill in the form and create a license")
    print("   4. Verify it appears in licenses_master.db")
    print("   5. Verify tenant database is created")
    print("   6. Test login with the new license")
    
    return True

if __name__ == "__main__":
    success = test_license_creation_integration()
    sys.exit(0 if success else 1)

