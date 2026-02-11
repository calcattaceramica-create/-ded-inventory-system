import sqlite3

conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')
cursor = conn.cursor()

# Search for licenses matching the patterns from the image
patterns = ['121B', '4A1B', '822A', '6927', 'DED-']

print("="*80)
print("🔍 Searching for licenses from Control Panel image...")
print("="*80)

for pattern in patterns:
    cursor.execute(f"SELECT license_key, client_name, admin_username, is_active, expires_at FROM licenses WHERE license_key LIKE '{pattern}%'")
    results = cursor.fetchall()
    
    if results:
        print(f"\n📋 Licenses starting with '{pattern}':")
        for lic in results:
            print(f"   Key: {lic[0]}")
            print(f"   Client: {lic[1]}")
            print(f"   Username: {lic[2]}")
            print(f"   Active: {'✅' if lic[3] else '❌'}")
            print(f"   Expires: {lic[4]}")
            print()

# Also get all licenses to see what we have
print("="*80)
print("📋 ALL LICENSES IN DATABASE:")
print("="*80)
cursor.execute("SELECT license_key, client_name, admin_username, is_active FROM licenses ORDER BY created_at DESC")
all_licenses = cursor.fetchall()

for i, lic in enumerate(all_licenses, 1):
    print(f"{i}. {lic[0]} | {lic[1]} | User: {lic[2]} | Active: {'✅' if lic[3] else '❌'}")

conn.close()
print("="*80)

