"""
اختبار تسجيل الخروج
Test logout functionality
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

print("=" * 80)
print("🔍 اختبار تسجيل الخروج")
print("🔍 Testing Logout Functionality")
print("=" * 80)

# Create session with retry strategy
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

base_url = "http://127.0.0.1:5000"

print("\n📝 الخطوة 1: محاولة تسجيل الدخول...")
print("📝 Step 1: Attempting login...")

# Login
login_data = {
    'username': 'admin',
    'password': 'admin123',
    'license_key': 'DEMO-LICENSE-KEY-2024'
}

try:
    response = session.post(f"{base_url}/auth/login", data=login_data, allow_redirects=False)
    print(f"   Status Code: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
    
    if response.status_code in [200, 302]:
        print("   ✅ تم تسجيل الدخول بنجاح!")
        print("   ✅ Login successful!")
    else:
        print("   ❌ فشل تسجيل الدخول!")
        print("   ❌ Login failed!")
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ خطأ: {e}")

print("\n📝 الخطوة 2: التحقق من الجلسة...")
print("📝 Step 2: Checking session...")

try:
    response = session.get(f"{base_url}/index", allow_redirects=False)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ الجلسة نشطة - يمكن الوصول للصفحة الرئيسية")
        print("   ✅ Session active - can access dashboard")
    elif response.status_code == 302:
        print("   ⚠️  تم إعادة التوجيه - قد تكون الجلسة غير نشطة")
        print("   ⚠️  Redirected - session may not be active")
    else:
        print(f"   ❌ خطأ: {response.status_code}")
except Exception as e:
    print(f"   ❌ خطأ: {e}")

print("\n📝 الخطوة 3: محاولة تسجيل الخروج...")
print("📝 Step 3: Attempting logout...")

try:
    response = session.get(f"{base_url}/auth/logout", allow_redirects=False)
    print(f"   Status Code: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
    
    if response.status_code == 302:
        location = response.headers.get('Location', '')
        print(f"   Redirect Location: {location}")
        
        if 'login' in location:
            print("   ✅ تم تسجيل الخروج بنجاح!")
            print("   ✅ Logout successful!")
        else:
            print("   ⚠️  تم إعادة التوجيه لكن ليس لصفحة تسجيل الدخول")
            print("   ⚠️  Redirected but not to login page")
    else:
        print("   ❌ فشل تسجيل الخروج!")
        print("   ❌ Logout failed!")
except Exception as e:
    print(f"   ❌ خطأ: {e}")

print("\n📝 الخطوة 4: التحقق من الجلسة بعد تسجيل الخروج...")
print("📝 Step 4: Checking session after logout...")

try:
    response = session.get(f"{base_url}/index", allow_redirects=False)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 302:
        location = response.headers.get('Location', '')
        if 'login' in location:
            print("   ✅ تم تسجيل الخروج بنجاح - لا يمكن الوصول للصفحة الرئيسية")
            print("   ✅ Logout successful - cannot access dashboard")
        else:
            print("   ⚠️  تم إعادة التوجيه لكن ليس لصفحة تسجيل الدخول")
            print("   ⚠️  Redirected but not to login page")
    elif response.status_code == 200:
        print("   ❌ فشل تسجيل الخروج - لا تزال الجلسة نشطة!")
        print("   ❌ Logout failed - session still active!")
    else:
        print(f"   ⚠️  Status Code: {response.status_code}")
except Exception as e:
    print(f"   ❌ خطأ: {e}")

print("\n" + "=" * 80)
print("✅ انتهى الاختبار!")
print("✅ Test completed!")
print("=" * 80)

print("\n📋 التوصيات:")
print("📋 Recommendations:")
print("\n1. إذا كان تسجيل الخروج يعمل في السكريبت لكن لا يعمل في المتصفح:")
print("   - المشكلة في الكاش (Cache) في المتصفح")
print("   - امسح الكوكيز: Ctrl + Shift + Delete")
print("\n2. إذا كان تسجيل الخروج لا يعمل في السكريبت:")
print("   - المشكلة في كود تسجيل الخروج")
print("   - تحقق من ملف: C:\\Users\\DELL\\Desktop\\DED_Portable_App\\app\\auth\\routes.py")
print("\n3. للاختبار اليدوي:")
print("   - اذهب إلى: http://127.0.0.1:5000/auth/logout")
print("   - يجب أن تُعاد توجيهك إلى صفحة تسجيل الدخول")

