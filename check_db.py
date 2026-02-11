import sqlite3
from pathlib import Path

db_path = Path('C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db')
print(f'Database: {db_path}')
print(f'Exists: {db_path.exists()}')
print()

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check if licenses table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='licenses'")
table_exists = cursor.fetchone()
print(f'Licenses table exists: {table_exists is not None}')
print()

if table_exists:
    # Get all licenses
    cursor.execute('SELECT license_key, client_name, is_active, expires_at FROM licenses')
    licenses = cursor.fetchall()
    print(f'Total licenses: {len(licenses)}')
    print()
    
    for lic in licenses:
        print(f'Key: {lic[0]}')
        print(f'Client: {lic[1]}')
        print(f'Active: {lic[2]}')
        print(f'Expires: {lic[3]}')
        print('---')

conn.close()

