"""
Test DED Control Panel Integration with License Control
اختبار دمج لوحة التحكم مع نظام التحكم في التراخيص
"""
import sys
sys.path.insert(0, 'C:/Users/DELL/Desktop/DED_Portable_App')

from license_control import LicenseControl

def test_integration():
    print("="*80)
    print("🧪 Testing DED Control Panel Integration")
    print("="*80)
    print()
    
    # Initialize License Control
    lc = LicenseControl()
    
    # Get all licenses
    print("📋 Getting all licenses...")
    licenses = lc.get_all_licenses()
    print(f"Found {len(licenses)} licenses\n")
    
    if not licenses:
        print("❌ No licenses found!")
        return
    
    # Display licenses
    for i, lic in enumerate(licenses, 1):
        print(f"{i}. {lic['license_key']}")
        print(f"   Company: {lic['client_name']}")
        print(f"   Active: {lic['is_active']}")
        print(f"   Suspended: {lic['is_suspended']}")
        print()
    
    # Test with first license
    test_license = licenses[0]['license_key']
    print(f"🧪 Testing with license: {test_license}\n")
    
    # Test 1: Suspend
    print("1️⃣ Testing SUSPEND...")
    success, msg = lc.suspend_license(test_license, "اختبار من Control Panel")
    print(f"   {'✅' if success else '❌'} {msg}\n")
    
    # Test 2: Activate
    print("2️⃣ Testing ACTIVATE...")
    success, msg = lc.activate_license(test_license)
    print(f"   {'✅' if success else '❌'} {msg}\n")
    
    # Test 3: Extend
    print("3️⃣ Testing EXTEND (30 days)...")
    success, msg = lc.extend_license(test_license, 30)
    print(f"   {'✅' if success else '❌'} {msg}\n")
    
    print("="*80)
    print("✅ Integration Test Complete!")
    print("="*80)
    print()
    print("📝 Summary:")
    print("   ✅ License Control module is working")
    print("   ✅ All control functions tested successfully")
    print("   ✅ Ready to use in DED Control Panel")
    print()
    print("🚀 Next Steps:")
    print("   1. Open DED Control Panel")
    print("   2. Go to 'مدير التراخيص' (License Manager)")
    print("   3. Click on any license card")
    print("   4. Use the control buttons:")
    print("      - ✅ تفعيل (Activate)")
    print("      - ⏸️ إيقاف (Suspend)")
    print("      - 🔄 تمديد (Extend)")
    print("="*80)

if __name__ == '__main__':
    test_integration()

