"""
Check if license 6F10-C3E8-398D-C858 exists in databases
"""
import sqlite3
from pathlib import Path

license_key = "6F10-C3E8-398D-C858"

print("=" * 80)
print(f"🔍 Checking License: {license_key}")
print("=" * 80)
print()

# Check in licenses_master.db
print("1️⃣ Checking licenses_master.db...")
try:
    conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM licenses WHERE license_key = ?', (license_key,))
    result = cursor.fetchone()
    
    if result:
        print(f"   ✅ FOUND in licenses_master.db")
        print(f"   License Key: {result[1]}")
        print(f"   Client: {result[2]}")
        print(f"   Active: {result[3]}")
        print(f"   Suspended: {result[4]}")
    else:
        print(f"   ❌ NOT FOUND in licenses_master.db")
    conn.close()
except Exception as e:
    print(f"   ❌ Error: {e}")
print()

# Check in erp_system.db
print("2️⃣ Checking erp_system.db...")
try:
    conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM licenses WHERE license_key = ?', (license_key,))
    result = cursor.fetchone()
    
    if result:
        print(f"   ✅ FOUND in erp_system.db")
        print(f"   License Key: {result[1]}")
        print(f"   Client: {result[2]}")
        print(f"   Active: {result[3]}")
        print(f"   Suspended: {result[4]}")
    else:
        print(f"   ❌ NOT FOUND in erp_system.db")
    conn.close()
except Exception as e:
    print(f"   ❌ Error: {e}")
print()

# Check for tenant database
print("3️⃣ Checking for tenant database...")
tenant_key = license_key.replace('-', '').lower()
tenant_db = f'C:/Users/DELL/Desktop/DED_Portable_App/tenant_{tenant_key}.db'
tenant_path = Path(tenant_db)

if tenant_path.exists():
    print(f"   ✅ Tenant database EXISTS: tenant_{tenant_key}.db")
else:
    print(f"   ❌ Tenant database NOT FOUND: tenant_{tenant_key}.db")
print()

# List all licenses in licenses_master.db
print("4️⃣ All licenses in licenses_master.db:")
try:
    conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')
    cursor = conn.cursor()
    cursor.execute('SELECT license_key, client_name, is_active, is_suspended FROM licenses')
    results = cursor.fetchall()
    
    for i, r in enumerate(results, 1):
        print(f"   {i}. {r[0]} | {r[1]} | Active:{r[2]} | Suspended:{r[3]}")
    conn.close()
except Exception as e:
    print(f"   ❌ Error: {e}")
print()

print("=" * 80)
print("🔍 DIAGNOSIS:")
print("=" * 80)
print()
print("The license 6F10-C3E8-398D-C858 is shown in Control Panel but:")
print("- If NOT in licenses_master.db → Need to add it")
print("- If NOT in tenant database → Need to create tenant DB")
print("- Control Panel might be reading from old JSON file")
print()
print("=" * 80)

