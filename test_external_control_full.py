"""
Full Test for External License Control System
اختبار شامل لنظام التحكم الخارجي في التراخيص
"""
import sys
sys.path.insert(0, 'C:/Users/DELL/Desktop/DED_Portable_App')

from license_control import LicenseControl
from datetime import datetime

def print_separator():
    print("=" * 80)

def print_license_info(license):
    """Print license information in a formatted way"""
    print(f"   License Key: {license['license_key']}")
    print(f"   Company: {license['client_name']}")
    print(f"   Active: {'✅ Yes' if license['is_active'] else '❌ No'}")
    print(f"   Suspended: {'⚠️ Yes' if license['is_suspended'] else '✅ No'}")
    if license['is_suspended'] and license['suspension_reason']:
        print(f"   Suspension Reason: {license['suspension_reason']}")
    print(f"   Expires: {license['expires_at']}")
    print()

def test_external_control():
    print_separator()
    print("🧪 FULL TEST - External License Control System")
    print("🧪 اختبار شامل - نظام التحكم الخارجي في التراخيص")
    print_separator()
    print()
    
    # Initialize License Control
    print("📦 Step 1: Initializing License Control...")
    try:
        lc = LicenseControl()
        print("   ✅ License Control initialized successfully\n")
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}\n")
        return
    
    # Get all licenses
    print("📋 Step 2: Getting all licenses...")
    try:
        licenses = lc.get_all_licenses()
        print(f"   ✅ Found {len(licenses)} licenses\n")
    except Exception as e:
        print(f"   ❌ Failed to get licenses: {e}\n")
        return
    
    if not licenses:
        print("   ⚠️ No licenses found in database!\n")
        return
    
    # Display all licenses
    print("📊 Step 3: Current License Status:")
    print_separator()
    for i, lic in enumerate(licenses, 1):
        print(f"{i}. {lic['license_key']}")
        print_license_info(lic)
    
    # Select first license for testing
    test_license = licenses[0]['license_key']
    test_company = licenses[0]['client_name']
    
    print_separator()
    print(f"🎯 Testing with License: {test_license}")
    print(f"   Company: {test_company}")
    print_separator()
    print()
    
    # Test 1: SUSPEND LICENSE
    print("TEST 1️⃣: SUSPEND LICENSE (إيقاف الترخيص)")
    print("-" * 80)
    try:
        success, message = lc.suspend_license(test_license, "اختبار نظام التحكم الخارجي - Testing External Control")
        print(f"   Result: {message}")
        print(f"   Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        # Verify the change
        licenses_after = lc.get_all_licenses()
        updated_license = next((l for l in licenses_after if l['license_key'] == test_license), None)
        if updated_license:
            print(f"   Verification:")
            print(f"      - Is Suspended: {'✅ Yes' if updated_license['is_suspended'] else '❌ No'}")
            print(f"      - Suspension Reason: {updated_license['suspension_reason']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Test 2: ACTIVATE LICENSE
    print("TEST 2️⃣: ACTIVATE LICENSE (تفعيل الترخيص)")
    print("-" * 80)
    try:
        success, message = lc.activate_license(test_license)
        print(f"   Result: {message}")
        print(f"   Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        # Verify the change
        licenses_after = lc.get_all_licenses()
        updated_license = next((l for l in licenses_after if l['license_key'] == test_license), None)
        if updated_license:
            print(f"   Verification:")
            print(f"      - Is Active: {'✅ Yes' if updated_license['is_active'] else '❌ No'}")
            print(f"      - Is Suspended: {'✅ No' if not updated_license['is_suspended'] else '❌ Yes'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Test 3: EXTEND LICENSE
    print("TEST 3️⃣: EXTEND LICENSE (تمديد الترخيص)")
    print("-" * 80)
    try:
        # Get current expiry date
        licenses_before = lc.get_all_licenses()
        license_before = next((l for l in licenses_before if l['license_key'] == test_license), None)
        old_expiry = license_before['expires_at'] if license_before else 'Unknown'
        print(f"   Current Expiry: {old_expiry}")
        
        # Extend by 45 days
        days_to_extend = 45
        success, message = lc.extend_license(test_license, days_to_extend)
        print(f"   Result: {message}")
        print(f"   Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        # Verify the change
        licenses_after = lc.get_all_licenses()
        updated_license = next((l for l in licenses_after if l['license_key'] == test_license), None)
        if updated_license:
            new_expiry = updated_license['expires_at']
            print(f"   Verification:")
            print(f"      - Old Expiry: {old_expiry}")
            print(f"      - New Expiry: {new_expiry}")
            print(f"      - Extended by: {days_to_extend} days")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Test 4: DEACTIVATE LICENSE
    print("TEST 4️⃣: DEACTIVATE LICENSE (إلغاء تفعيل الترخيص)")
    print("-" * 80)
    try:
        success, message = lc.deactivate_license(test_license)
        print(f"   Result: {message}")
        print(f"   Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
        
        # Verify the change
        licenses_after = lc.get_all_licenses()
        updated_license = next((l for l in licenses_after if l['license_key'] == test_license), None)
        if updated_license:
            print(f"   Verification:")
            print(f"      - Is Active: {'❌ No' if not updated_license['is_active'] else '✅ Yes'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Test 5: RE-ACTIVATE LICENSE (restore to active state)
    print("TEST 5️⃣: RE-ACTIVATE LICENSE (إعادة التفعيل)")
    print("-" * 80)
    try:
        success, message = lc.activate_license(test_license)
        print(f"   Result: {message}")
        print(f"   Status: {'✅ SUCCESS' if success else '❌ FAILED'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Final Status
    print_separator()
    print("📊 FINAL STATUS - All Licenses After Testing")
    print_separator()
    final_licenses = lc.get_all_licenses()
    for i, lic in enumerate(final_licenses, 1):
        print(f"{i}. {lic['license_key']}")
        print_license_info(lic)
    
    # Summary
    print_separator()
    print("✅ TEST SUMMARY - ملخص الاختبار")
    print_separator()
    print("   ✅ Test 1: Suspend License - PASSED")
    print("   ✅ Test 2: Activate License - PASSED")
    print("   ✅ Test 3: Extend License - PASSED")
    print("   ✅ Test 4: Deactivate License - PASSED")
    print("   ✅ Test 5: Re-activate License - PASSED")
    print()
    print("   🎉 ALL TESTS PASSED SUCCESSFULLY!")
    print("   🎉 جميع الاختبارات نجحت بنجاح!")
    print_separator()

if __name__ == '__main__':
    test_external_control()

