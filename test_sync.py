import sqlite3
from pathlib import Path
from datetime import datetime

db_path = Path('C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db')

print("Checking recent licenses in database...")
print("="*60)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get all licenses ordered by creation date
cursor.execute('''
    SELECT license_key, client_name, client_company, created_at, expires_at, is_active
    FROM licenses
    ORDER BY created_at DESC
    LIMIT 10
''')

licenses = cursor.fetchall()

print(f"Total recent licenses: {len(licenses)}\n")

for lic in licenses:
    print(f"Key: {lic[0]}")
    print(f"Client Name: {lic[1]}")
    print(f"Company: {lic[2]}")
    print(f"Created: {lic[3]}")
    print(f"Expires: {lic[4]}")
    print(f"Active: {lic[5]}")
    print("-"*60)

conn.close()

