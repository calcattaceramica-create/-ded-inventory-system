"""
Add missing license 6F10-C3E8-398D-C858 to licenses_master.db and create tenant DB
"""
import sqlite3
import hashlib
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

license_key = "6F10-C3E8-398D-C858"
client_name = "calc"  # From the screenshot
username = "ahmed"    # From the screenshot

# Generate license hash
license_hash = hashlib.sha256(license_key.encode()).hexdigest()

print("=" * 80)
print(f"🔧 Adding Missing License: {license_key}")
print("=" * 80)
print()

# Step 1: Add to licenses_master.db
print("1️⃣ Adding license to licenses_master.db...")
try:
    conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')
    cursor = conn.cursor()
    
    # Check if already exists
    cursor.execute('SELECT * FROM licenses WHERE license_key = ?', (license_key,))
    existing = cursor.fetchone()
    
    if existing:
        print(f"   ⚠️ License already exists in database!")
    else:
        # Add the license
        expires_at = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        admin_password_hash = generate_password_hash('admin123')

        cursor.execute('''
            INSERT INTO licenses (
                license_key, license_hash, client_name, is_active, is_suspended,
                suspension_reason, expires_at, created_at, admin_username, admin_password_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            license_key,
            license_hash,
            client_name,
            1,  # is_active
            0,  # is_suspended
            None,  # suspension_reason
            expires_at,
            created_at,
            username,
            admin_password_hash
        ))
        
        conn.commit()
        print(f"   ✅ License added successfully!")
        print(f"   - License Key: {license_key}")
        print(f"   - Client: {client_name}")
        print(f"   - Active: Yes")
        print(f"   - Expires: {expires_at}")
    
    conn.close()
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Step 2: Create tenant database
print("2️⃣ Creating tenant database...")
try:
    tenant_key = license_key.replace('-', '').lower()
    tenant_db = f'C:/Users/DELL/Desktop/DED_Portable_App/tenant_{tenant_key}.db'
    
    conn = sqlite3.connect(tenant_db)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role_id INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create roles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            permissions TEXT
        )
    ''')
    
    # Add admin role
    cursor.execute('''
        INSERT OR IGNORE INTO roles (id, name, permissions)
        VALUES (1, 'admin', 'all')
    ''')
    
    # Add admin user
    password_hash = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password_hash, role_id, is_active)
        VALUES (?, ?, 1, 1)
    ''', (username, password_hash))
    
    conn.commit()
    conn.close()
    
    print(f"   ✅ Tenant database created successfully!")
    print(f"   - Database: tenant_{tenant_key}.db")
    print(f"   - Username: {username}")
    print(f"   - Password: admin123")
    print(f"   - Role: admin")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Step 3: Verify
print("3️⃣ Verifying...")
try:
    # Check licenses_master.db
    conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')
    cursor = conn.cursor()
    cursor.execute('SELECT license_key, client_name, is_active, expires_at FROM licenses WHERE license_key = ?', (license_key,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        print(f"   ✅ License found in licenses_master.db")
        print(f"      Key: {result[0]}")
        print(f"      Client: {result[1]}")
        print(f"      Active: {result[2]}")
        print(f"      Expires: {result[3]}")
    else:
        print(f"   ❌ License NOT found in licenses_master.db")
    
    # Check tenant database
    import os
    tenant_key = license_key.replace('-', '').lower()
    tenant_db = f'C:/Users/DELL/Desktop/DED_Portable_App/tenant_{tenant_key}.db'
    
    if os.path.exists(tenant_db):
        print(f"   ✅ Tenant database exists: tenant_{tenant_key}.db")
        
        # Check user
        conn = sqlite3.connect(tenant_db)
        cursor = conn.cursor()
        cursor.execute('SELECT username, is_active FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            print(f"      ✅ User '{user[0]}' exists (Active: {user[1]})")
        else:
            print(f"      ❌ User not found")
    else:
        print(f"   ❌ Tenant database NOT found")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print()
print("=" * 80)
print("✅ DONE! License is now ready to use!")
print("=" * 80)
print()
print("📝 Login Credentials:")
print(f"   License Key: {license_key}")
print(f"   Username: {username}")
print(f"   Password: admin123")
print()
print("=" * 80)

