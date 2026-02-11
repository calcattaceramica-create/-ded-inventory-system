"""
Test License Control API
اختبار API التحكم في التراخيص
"""
import requests
import json

API_URL = "http://127.0.0.1:5001/api"

def print_header(title):
    print("\n" + "="*80)
    print(f"🔧 {title}")
    print("="*80)

def get_all_licenses():
    """Get all licenses"""
    print_header("Getting All Licenses")
    
    try:
        response = requests.get(f"{API_URL}/licenses", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                licenses = data['licenses']
                print(f"✅ Found {len(licenses)} licenses:")
                print()
                
                for i, lic in enumerate(licenses, 1):
                    print(f"{i}. {lic['license_key']}")
                    print(f"   Client: {lic['client_name']}")
                    print(f"   Username: {lic['admin_username']}")
                    print(f"   Active: {'✅' if lic['is_active'] else '❌'}")
                    print(f"   Suspended: {'⚠️ Yes' if lic['is_suspended'] else '✅ No'}")
                    print(f"   Expires: {lic['expires_at']}")
                    print()
                
                return licenses
            else:
                print(f"❌ Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("⚠️ Make sure the API server is running!")
        print("   Run: python license_control_api.py")
    
    return []

def suspend_license(license_key, reason="Test suspension"):
    """Suspend a license"""
    print_header(f"Suspending License: {license_key}")
    
    try:
        response = requests.post(
            f"{API_URL}/license/{license_key}/suspend",
            json={'reason': reason},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ {data['message']}")
            else:
                print(f"❌ Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def activate_license(license_key):
    """Activate a license"""
    print_header(f"Activating License: {license_key}")
    
    try:
        response = requests.post(
            f"{API_URL}/license/{license_key}/activate",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ {data['message']}")
            else:
                print(f"❌ Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def extend_license(license_key, days=30):
    """Extend license"""
    print_header(f"Extending License: {license_key}")
    
    try:
        response = requests.post(
            f"{API_URL}/license/{license_key}/extend",
            json={'days': days},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ {data['message']}")
                print(f"   New expiration: {data['new_expires']}")
            else:
                print(f"❌ Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("="*80)
    print("🧪 License Control API Test")
    print("="*80)
    
    # Get all licenses
    licenses = get_all_licenses()
    
    if licenses:
        # Test with first license
        test_license = licenses[0]['license_key']
        
        # Test suspend
        suspend_license(test_license, "Testing suspension from API")
        
        # Get licenses again to see the change
        get_all_licenses()
        
        # Test activate
        activate_license(test_license)
        
        # Get licenses again
        get_all_licenses()
        
        # Test extend
        extend_license(test_license, 60)
        
        # Final check
        get_all_licenses()
    
    print("="*80)
    print("✅ Test Complete!")
    print("="*80)

