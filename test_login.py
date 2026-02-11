import requests

# Login credentials
url = "http://127.0.0.1:5000/auth/login"
data = {
    "username": "testuser",
    "password": "test123",
    "license_key": "0531-E2D1-2016-3258"
}

print("="*80)
print("🔐 Testing Login...")
print("="*80)
print(f"URL: {url}")
print(f"Username: {data['username']}")
print(f"Password: {data['password']}")
print(f"License Key: {data['license_key']}")
print("="*80)
print()

try:
    # Create session to handle cookies
    session = requests.Session()
    
    # First, get the login page to get any CSRF tokens
    print("📥 Getting login page...")
    response = session.get(url)
    print(f"Status: {response.status_code}")
    
    # Now try to login
    print()
    print("📤 Attempting login...")
    response = session.post(url, data=data, allow_redirects=False)
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 302:
        print()
        print("✅ Login successful! (Redirect detected)")
        print(f"Redirect to: {response.headers.get('Location', 'Unknown')}")
    elif response.status_code == 200:
        print()
        if "مرحباً" in response.text or "Welcome" in response.text:
            print("✅ Login successful!")
        elif "غير صحيح" in response.text or "invalid" in response.text.lower():
            print("❌ Login failed - Invalid credentials or license")
            # Print relevant error messages
            if "مفتاح الترخيص" in response.text:
                print("   Error: License key issue")
            if "اسم المستخدم" in response.text:
                print("   Error: Username issue")
            if "كلمة المرور" in response.text:
                print("   Error: Password issue")
        else:
            print("⚠️ Login response unclear")
            print(f"Response length: {len(response.text)} characters")
    else:
        print(f"❌ Unexpected status code: {response.status_code}")
    
    print("="*80)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("="*80)

