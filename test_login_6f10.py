"""
Test login with license 6F10-C3E8-398D-C858
"""
import requests
import time

# Start Flask app first (if not running)
print("=" * 80)
print("🧪 Testing Login with License: 6F10-C3E8-398D-C858")
print("=" * 80)
print()

# Test credentials
license_key = "6F10-C3E8-398D-C858"
username = "ahmed"
password = "admin123"

print("📝 Test Credentials:")
print(f"   License Key: {license_key}")
print(f"   Username: {username}")
print(f"   Password: {password}")
print()

# Wait a bit for Flask to be ready
print("⏳ Waiting for Flask app to be ready...")
time.sleep(2)

# Test login
print("🔐 Attempting login...")
try:
    url = "http://127.0.0.1:5000/auth/login"
    
    data = {
        'license_key': license_key,
        'username': username,
        'password': password
    }
    
    response = requests.post(url, data=data, allow_redirects=False)
    
    print(f"   Status Code: {response.status_code}")
    print(f"   Response Headers: {dict(response.headers)}")
    
    if response.status_code == 302:
        redirect_location = response.headers.get('Location', '')
        print(f"   Redirect Location: {redirect_location}")
        
        if '/index' in redirect_location or '/dashboard' in redirect_location:
            print()
            print("   ✅ LOGIN SUCCESSFUL!")
            print("   ✅ تم تسجيل الدخول بنجاح!")
        else:
            print()
            print("   ❌ LOGIN FAILED - Redirected to:", redirect_location)
    elif response.status_code == 200:
        if 'Invalid' in response.text or 'خطأ' in response.text:
            print()
            print("   ❌ LOGIN FAILED - Invalid credentials")
        else:
            print()
            print("   ✅ LOGIN SUCCESSFUL!")
    else:
        print()
        print(f"   ❌ Unexpected status code: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print()
    print("   ❌ ERROR: Flask app is not running!")
    print("   Please start the Flask app first:")
    print("   python C:/Users/DELL/Desktop/DED_Portable_App/run.py")
except Exception as e:
    print()
    print(f"   ❌ ERROR: {e}")

print()
print("=" * 80)

