import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import hashlib
import secrets

# Database path - use licenses_master.db (the correct one)
db_path = Path('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')

# Generate a 16-character license key
def create_license_key(company):
    timestamp = datetime.now().isoformat()
    random_part = secrets.token_hex(8)  # 8 bytes = 16 hex characters
    
    data = f"{company}-{timestamp}-{random_part}"
    hash_obj = hashlib.sha256(data.encode())
    
    # Format as XXXX-XXXX-XXXX-XXXX (16 characters total)
    full_key = hash_obj.hexdigest()[:16].upper()
    formatted_key = '-'.join([full_key[i:i+4] for i in range(0, 16, 4)])
    
    return formatted_key

# License details
license_key = create_license_key("TestCompany")
license_hash = hashlib.sha256(license_key.encode()).hexdigest()
client_name = "testuser"
client_company = "Test Company"
admin_username = "testuser"
admin_password = "test123"
admin_password_hash = generate_password_hash(admin_password)
created_at = datetime.now()
expires_at = created_at + timedelta(days=365)

print("="*80)
print("🔑 Creating Test License...")
print("="*80)
print(f"License Key: {license_key}")
print(f"Company: {client_company}")
print(f"Username: {admin_username}")
print(f"Password: {admin_password}")
print(f"Created: {created_at}")
print(f"Expires: {expires_at}")
print("="*80)

# Connect to database
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check if license already exists
cursor.execute('SELECT license_key FROM licenses WHERE license_key = ?', (license_key,))
existing = cursor.fetchone()

if existing:
    print(f"⚠️ License already exists: {license_key}")
else:
    # Insert license (using correct column names from licenses_master.db)
    cursor.execute('''
        INSERT INTO licenses (
            license_key, license_hash, client_name, client_company, client_email, client_phone,
            admin_username, admin_password_hash,
            max_users, is_active, is_suspended, suspension_reason,
            created_at, expires_at, last_check, license_type, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        license_key,
        license_hash,
        client_name,
        client_company,
        f"{admin_username}@test.com",
        "1234567890",
        admin_username,
        admin_password_hash,
        10,  # max_users
        1,   # is_active
        0,   # is_suspended
        None,  # suspension_reason,
        created_at.strftime('%Y-%m-%d %H:%M:%S'),
        expires_at.strftime('%Y-%m-%d %H:%M:%S'),
        created_at.strftime('%Y-%m-%d %H:%M:%S'),  # last_check
        "standard",  # license_type
        "Test license created by script"  # notes
    ))
    
    conn.commit()
    print("✅ License created successfully!")

# Verify license was created
cursor.execute('SELECT * FROM licenses WHERE license_key = ?', (license_key,))
result = cursor.fetchone()

if result:
    print("="*80)
    print("✅ License verified in database!")
    print("="*80)
    print(f"License Key: {result[1]}")
    print(f"Client Name: {result[2]}")
    print(f"Company: {result[3]}")
    print(f"Username: {result[6]}")
    print(f"Active: {result[8]}")
    print(f"Expires: {result[12]}")
    print("="*80)
else:
    print("❌ License NOT found in database!")

conn.close()

print()
print("🚀 Now you can login with:")
print(f"   Username: {admin_username}")
print(f"   Password: {admin_password}")
print(f"   License Key: {license_key}")
print()
print("📝 Login URL: http://127.0.0.1:5000/auth/login")
print("="*80)

