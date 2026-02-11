import sys
sys.path.insert(0, 'C:/Users/DELL/Desktop/DED_Portable_App')

from license_control import LicenseControl

lc = LicenseControl()

print("="*80)
print("Testing License Control")
print("="*80)

# Get licenses
licenses = lc.get_all_licenses()
print(f"\nFound {len(licenses)} licenses\n")

for i, lic in enumerate(licenses, 1):
    print(f"{i}. {lic['license_key']}")
    print(f"   Active: {lic['is_active']}")
    print(f"   Suspended: {lic['is_suspended']}")
    print()

if licenses:
    test_key = licenses[0]['license_key']
    print(f"Testing with: {test_key}\n")
    
    # Test suspend
    print("1. Suspending...")
    success, msg = lc.suspend_license(test_key, "Test")
    print(f"   {msg}\n")
    
    # Test activate
    print("2. Activating...")
    success, msg = lc.activate_license(test_key)
    print(f"   {msg}\n")
    
    # Test extend
    print("3. Extending...")
    success, msg = lc.extend_license(test_key, 30)
    print(f"   {msg}\n")

print("="*80)
print("Test Complete!")
print("="*80)

