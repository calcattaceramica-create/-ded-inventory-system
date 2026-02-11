import sqlite3
import requests

print("="*80)
print("📊 COMPREHENSIVE LICENSE TEST REPORT")
print("="*80)
print()

# Test 1: Check licenses_master.db (used by main app)
print("1️⃣ LICENSES IN licenses_master.db (Main App Database):")
print("-"*80)
conn1 = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')
cursor1 = conn1.cursor()
cursor1.execute('SELECT license_key, client_name, admin_username, is_active FROM licenses')
master_licenses = cursor1.fetchall()
conn1.close()

for i, lic in enumerate(master_licenses, 1):
    print(f"   {i}. {lic[0]} | {lic[1]} | User: {lic[2]} | Active: {'✅' if lic[3] else '❌'}")

print()

# Test 2: Check erp_system.db (used by Control Panel)
print("2️⃣ LICENSES IN erp_system.db (Control Panel Database):")
print("-"*80)
conn2 = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db')
cursor2 = conn2.cursor()
cursor2.execute('SELECT license_key, client_name, client_company FROM licenses')
erp_licenses = cursor2.fetchall()
conn2.close()

for i, lic in enumerate(erp_licenses, 1):
    print(f"   {i}. {lic[0]} | {lic[1]} | Company: {lic[2]}")

print()

# Test 3: Try to login with licenses from licenses_master.db
print("3️⃣ LOGIN TEST WITH licenses_master.db LICENSES:")
print("-"*80)

url = "http://127.0.0.1:5000/auth/login"
success_count = 0

for lic in master_licenses:
    license_key = lic[0]
    username = lic[2]
    
    # Try with admin123 password
    data = {
        "username": username,
        "password": "admin123",
        "license_key": license_key
    }
    
    try:
        session = requests.Session()
        response = session.post(url, data=data, allow_redirects=False, timeout=5)
        
        if response.status_code == 302:
            redirect = response.headers.get('Location', '')
            if '/index' in redirect:
                print(f"   ✅ {license_key} | User: {username} | SUCCESS → {redirect}")
                success_count += 1
            else:
                print(f"   ⚠️ {license_key} | User: {username} | Redirect → {redirect}")
        else:
            print(f"   ❌ {license_key} | User: {username} | FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ {license_key} | User: {username} | ERROR: {str(e)[:40]}")

print()

# Test 4: Try to login with licenses from erp_system.db
print("4️⃣ LOGIN TEST WITH erp_system.db LICENSES:")
print("-"*80)

for lic in erp_licenses:
    license_key = lic[0]
    # Try with admin username
    data = {
        "username": "admin",
        "password": "admin123",
        "license_key": license_key
    }
    
    try:
        session = requests.Session()
        response = session.post(url, data=data, allow_redirects=False, timeout=5)
        
        if response.status_code == 302:
            redirect = response.headers.get('Location', '')
            if '/index' in redirect:
                print(f"   ✅ {license_key} | SUCCESS → {redirect}")
            else:
                print(f"   ⚠️ {license_key} | Redirect → {redirect}")
        else:
            print(f"   ❌ {license_key} | FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ {license_key} | ERROR: {str(e)[:40]}")

print()
print("="*80)
print("📊 SUMMARY:")
print("="*80)
print(f"✅ Licenses in licenses_master.db: {len(master_licenses)}")
print(f"✅ Licenses in erp_system.db: {len(erp_licenses)}")
print(f"✅ Successful logins: {success_count}/{len(master_licenses)}")
print()
print("⚠️ ISSUE: Control Panel shows licenses from erp_system.db")
print("⚠️ ISSUE: Main app uses licenses_master.db")
print("⚠️ SOLUTION: Need to sync Control Panel to use licenses_master.db")
print("="*80)

