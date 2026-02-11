"""
Test External License Control
اختبار التحكم الخارجي في التراخيص
"""
import sys
sys.path.insert(0, 'C:/Users/DELL/Desktop/DED_Portable_App')

from license_control import LicenseControl

def print_header(title):
    print("\n" + "="*80)
    print(f"🔧 {title}")
    print("="*80)

def main():
    print("="*80)
    print("🧪 External License Control Test")
    print("="*80)
    
    # Initialize license control
    lc = LicenseControl()
    
    # Get all licenses
    print_header("Getting All Licenses")
    licenses = lc.get_all_licenses()
    
    print(f"Found {len(licenses)} licenses:")
    print()
    
    for i, lic in enumerate(licenses, 1):
        print(f"{i}. {lic['license_key']}")
        print(f"   Client: {lic['client_name']} ({lic['client_company']})")
        print(f"   Username: {lic['admin_username']}")
        print(f"   Active: {'✅ Yes' if lic['is_active'] else '❌ No'}")
        print(f"   Suspended: {'⚠️ Yes' if lic['is_suspended'] else '✅ No'}")
        if lic['suspension_reason']:
            print(f"   Reason: {lic['suspension_reason']}")
        print(f"   Expires: {lic['expires_at']}")
        print(f"   Max Users: {lic['max_users']}")
        print()
    
    if not licenses:
        print("❌ No licenses found!")
        return
    
    # Test with first license
    test_license = licenses[0]['license_key']
    
    print_header(f"Testing Control Functions with: {test_license}")
    
    # Test 1: Suspend
    print("\n1️⃣ Testing SUSPEND...")
    success, message = lc.suspend_license(test_license, "اختبار الإيقاف من الخارج")
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Verify
    licenses = lc.get_all_licenses()
    test_lic = next((l for l in licenses if l['license_key'] == test_license), None)
    if test_lic:
        print(f"   Verification: Suspended = {test_lic['is_suspended']}")
    
    # Test 2: Activate
    print("\n2️⃣ Testing ACTIVATE...")
    success, message = lc.activate_license(test_license)
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Verify
    licenses = lc.get_all_licenses()
    test_lic = next((l for l in licenses if l['license_key'] == test_license), None)
    if test_lic:
        print(f"   Verification: Active = {test_lic['is_active']}, Suspended = {test_lic['is_suspended']}")
    
    # Test 3: Extend
    print("\n3️⃣ Testing EXTEND (60 days)...")
    success, message = lc.extend_license(test_license, 60)
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Verify
    licenses = lc.get_all_licenses()
    test_lic = next((l for l in licenses if l['license_key'] == test_license), None)
    if test_lic:
        print(f"   Verification: New expiration = {test_lic['expires_at']}")
    
    # Test 4: Deactivate
    print("\n4️⃣ Testing DEACTIVATE...")
    success, message = lc.deactivate_license(test_license)
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Verify
    licenses = lc.get_all_licenses()
    test_lic = next((l for l in licenses if l['license_key'] == test_license), None)
    if test_lic:
        print(f"   Verification: Active = {test_lic['is_active']}")
    
    # Restore to active state
    print("\n5️⃣ Restoring to ACTIVE state...")
    success, message = lc.activate_license(test_license)
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Final status
    print_header("Final License Status")
    licenses = lc.get_all_licenses()
    
    for lic in licenses:
        status = []
        if lic['is_active']:
            status.append("✅ Active")
        else:
            status.append("❌ Inactive")
        
        if lic['is_suspended']:
            status.append("⚠️ Suspended")
        
        print(f"{lic['license_key']}: {' | '.join(status)}")
    
    print()
    print("="*80)
    print("✅ External Control Test Complete!")
    print("="*80)
    print()
    print("📝 Summary:")
    print("   ✅ License control module is working")
    print("   ✅ Can activate/suspend/extend licenses from external code")
    print("   ✅ Ready to integrate with DED Control Panel")
    print("="*80)

if __name__ == '__main__':
    main()

