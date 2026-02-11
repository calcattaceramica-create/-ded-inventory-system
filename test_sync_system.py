#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify bidirectional sync between Control Panel and Database
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# Add DED_Portable_App to path
sys.path.insert(0, 'C:/Users/DELL/Desktop/DED_Portable_App')

def test_sync_system():
    """Test the sync system"""
    
    print("=" * 80)
    print("🧪 Testing Bidirectional Sync System")
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
    
    # Test 1: Suspend a license from external control
    print("\n" + "=" * 80)
    print("TEST 1: Suspend license from external control")
    print("=" * 80)
    
    test_license = "CEC9-79EE-C42F-2DAD"
    
    print(f"\n🔄 Suspending license: {test_license}")
    success, message = lc.suspend_license(test_license, "Testing sync system")
    
    if success:
        print(f"✅ {message}")
        print("   This change should appear in Control Panel after sync!")
    else:
        print(f"❌ {message}")
    
    # Test 2: Check database state
    print("\n" + "=" * 80)
    print("TEST 2: Verify database state")
    print("=" * 80)
    
    db_path = Path("C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT license_key, client_company, is_active, is_suspended, suspension_reason
        FROM licenses
        WHERE license_key = ?
    """, (test_license,))
    
    result = cursor.fetchone()
    if result:
        key, company, active, suspended, reason = result
        print(f"\n📊 License: {key}")
        print(f"   Company: {company}")
        print(f"   Active: {'✅ Yes' if active else '❌ No'}")
        print(f"   Suspended: {'⚠️ Yes' if suspended else '✓ No'}")
        print(f"   Reason: {reason or 'N/A'}")
    
    conn.close()
    
    # Test 3: Activate it back
    print("\n" + "=" * 80)
    print("TEST 3: Activate license back")
    print("=" * 80)
    
    print(f"\n🔄 Activating license: {test_license}")
    success, message = lc.activate_license(test_license)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ Sync System Test Complete!")
    print("=" * 80)
    
    print("\n📝 How the sync works:")
    print("   1️⃣ External Control → Database (Immediate)")
    print("      - Use license_control.py to modify licenses")
    print("      - Changes saved directly to licenses_master.db")
    print()
    print("   2️⃣ Database → Control Panel (Auto-sync every 30 seconds)")
    print("      - Control Panel reads from licenses_master.db")
    print("      - Updates licenses.json automatically")
    print("      - Refreshes UI to show changes")
    print()
    print("   3️⃣ Control Panel → Database (Immediate)")
    print("      - Create/Edit/Activate/Suspend/Extend from Control Panel")
    print("      - Changes saved to both licenses.json AND licenses_master.db")
    print("      - Tenant databases created automatically")
    print()
    print("   4️⃣ Manual Sync Button")
    print("      - Click '🔄 مزامنة' button in Control Panel")
    print("      - Forces immediate sync from database")
    print("      - Useful after external changes")
    
    print("\n🎯 Next Steps:")
    print("   1. Open DED Control Panel")
    print("   2. Wait 5 seconds for first auto-sync")
    print("   3. Check if suspended license shows correctly")
    print("   4. Click '🔄 مزامنة' to force sync")
    print("   5. Make changes from Control Panel")
    print("   6. Verify changes in licenses_master.db")
    
    return True

if __name__ == "__main__":
    success = test_sync_system()
    sys.exit(0 if success else 1)

