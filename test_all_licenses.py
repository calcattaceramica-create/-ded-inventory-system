import requests
import sqlite3
from pathlib import Path

# Get all licenses from database
db_path = Path('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

cursor.execute('''
    SELECT license_key, client_name, admin_username, is_active, expires_at 
    FROM licenses 
    ORDER BY created_at DESC
''')
licenses = cursor.fetchall()
conn.close()

print("="*80)
print("🔐 Testing All Licenses")
print("="*80)
print(f"Found {len(licenses)} licenses in database")
print("="*80)
print()

# Test each license
url = "http://127.0.0.1:5000/auth/login"
results = []

for i, lic in enumerate(licenses, 1):
    license_key = lic[0]
    client_name = lic[1]
    admin_username = lic[2]
    is_active = lic[3]
    expires_at = lic[4]
    
    print(f"{i}. Testing License: {license_key}")
    print(f"   Client: {client_name}")
    print(f"   Username: {admin_username}")
    print(f"   Active: {'✅' if is_active else '❌'}")
    print(f"   Expires: {expires_at}")
    
    # Try to login with admin/admin123 (default password)
    data = {
        "username": admin_username,
        "password": "admin123",
        "license_key": license_key
    }
    
    try:
        session = requests.Session()
        response = session.post(url, data=data, allow_redirects=False, timeout=5)
        
        if response.status_code == 302:
            redirect = response.headers.get('Location', '')
            if '/index' in redirect or redirect.startswith('/'):
                print(f"   Result: ✅ LOGIN SUCCESS (Redirect to {redirect})")
                results.append((license_key, "✅ SUCCESS", admin_username))
            else:
                print(f"   Result: ⚠️ Redirect to {redirect}")
                results.append((license_key, "⚠️ REDIRECT", admin_username))
        elif response.status_code == 200:
            if "مرحباً" in response.text or "Welcome" in response.text:
                print(f"   Result: ✅ LOGIN SUCCESS")
                results.append((license_key, "✅ SUCCESS", admin_username))
            else:
                print(f"   Result: ❌ LOGIN FAILED")
                results.append((license_key, "❌ FAILED", admin_username))
        else:
            print(f"   Result: ❌ Status {response.status_code}")
            results.append((license_key, f"❌ {response.status_code}", admin_username))
    
    except Exception as e:
        print(f"   Result: ❌ ERROR: {str(e)[:50]}")
        results.append((license_key, "❌ ERROR", admin_username))
    
    print()

# Summary
print("="*80)
print("📊 SUMMARY")
print("="*80)
successful = [r for r in results if "SUCCESS" in r[1]]
failed = [r for r in results if "FAILED" in r[1] or "ERROR" in r[1]]

print(f"Total Licenses: {len(results)}")
print(f"✅ Successful: {len(successful)}")
print(f"❌ Failed: {len(failed)}")
print()

if successful:
    print("✅ Working Licenses:")
    for lic, status, user in successful:
        print(f"   - {lic} (User: {user})")
    print()

if failed:
    print("❌ Failed Licenses:")
    for lic, status, user in failed:
        print(f"   - {lic} (User: {user}) - {status}")

print("="*80)

