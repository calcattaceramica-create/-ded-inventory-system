import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Database path
db_path = Path('C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db')

# License details
license_key = "TEST-1234-5678-ABCD-EFGH-9012-3456-7890"  # 32 characters
client_name = "Test Company"
admin_username = "admin"
admin_password = "admin123"
expires_at = datetime.now() + timedelta(days=365)

print(f"Creating license...")
print(f"License Key: {license_key}")
print(f"Client: {client_name}")
print(f"Username: {admin_username}")
print(f"Password: {admin_password}")
print(f"Expires: {expires_at}")
print()

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Insert license
cursor.execute("""
    INSERT INTO licenses
    (license_key, client_name, client_email, admin_username, admin_password_hash,
     is_active, is_suspended, expires_at, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    license_key,
    client_name,
    f"{admin_username}@test.com",
    admin_username,
    generate_password_hash(admin_password),
    1,  # is_active
    0,  # is_suspended
    expires_at,
    datetime.now()
))

conn.commit()
print("✅ License created successfully!")

# Verify
cursor.execute("SELECT license_key, client_name, admin_username FROM licenses WHERE license_key = ?", (license_key,))
result = cursor.fetchone()
print(f"\nVerification:")
print(f"Key: {result[0]}")
print(f"Client: {result[1]}")
print(f"Username: {result[2]}")

conn.close()

print("\n" + "="*60)
print("🎉 USE THESE CREDENTIALS TO LOGIN:")
print("="*60)
print(f"Username: {admin_username}")
print(f"Password: {admin_password}")
print(f"License Key: {license_key}")
print("="*60)

