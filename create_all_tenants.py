"""
Create tenant databases for all licenses in licenses_master.db
إنشاء قواعد بيانات tenant لجميع التراخيص
"""
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash
from datetime import datetime

# Paths
app_dir = Path('C:/Users/DELL/Desktop/DED_Portable_App')
master_db = app_dir / 'licenses_master.db'

print("="*80)
print("🔧 Creating Tenant Databases for All Licenses")
print("="*80)
print()

# Get all licenses
conn = sqlite3.connect(str(master_db))
cursor = conn.cursor()

cursor.execute('''
    SELECT license_key, client_name, admin_username, admin_password_hash, is_active
    FROM licenses
    ORDER BY created_at DESC
''')
licenses = cursor.fetchall()
conn.close()

print(f"Found {len(licenses)} licenses")
print()

# Create tenant database for each license
for i, lic in enumerate(licenses, 1):
    license_key = lic[0]
    client_name = lic[1]
    admin_username = lic[2]
    admin_password_hash = lic[3]
    is_active = lic[4]
    
    # Generate tenant database name
    tenant_db_name = f"tenant_{license_key.replace('-', '').lower()}.db"
    tenant_db_path = app_dir / tenant_db_name
    
    print(f"{i}. License: {license_key}")
    print(f"   Client: {client_name}")
    print(f"   Username: {admin_username}")
    print(f"   Active: {'✅' if is_active else '❌'}")
    print(f"   Tenant DB: {tenant_db_name}")
    
    # Check if tenant database already exists
    if tenant_db_path.exists():
        print(f"   Status: ⚠️ Already exists - skipping")
        print()
        continue
    
    # Create tenant database
    try:
        tenant_conn = sqlite3.connect(str(tenant_db_path))
        tenant_cursor = tenant_conn.cursor()
        
        # Create users table
        tenant_cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(64) UNIQUE NOT NULL,
                email VARCHAR(120),
                password_hash VARCHAR(256) NOT NULL,
                full_name VARCHAR(128),
                phone VARCHAR(20),
                is_active BOOLEAN DEFAULT 1,
                is_admin BOOLEAN DEFAULT 0,
                language VARCHAR(10) DEFAULT 'ar',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        ''')
        
        # Create roles table
        tenant_cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(64) UNIQUE NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert admin user
        tenant_cursor.execute('''
            INSERT INTO users (
                username, email, password_hash, full_name,
                is_active, is_admin, language, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            admin_username,
            f"{admin_username}@{client_name.replace(' ', '').lower()}.com",
            admin_password_hash,
            client_name,
            1,  # is_active
            1,  # is_admin
            'ar',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        # Insert admin role
        tenant_cursor.execute('''
            INSERT INTO roles (name, description, created_at)
            VALUES (?, ?, ?)
        ''', (
            'Admin',
            'Administrator with full access',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        tenant_conn.commit()
        tenant_conn.close()
        
        print(f"   Status: ✅ Created successfully!")
        
    except Exception as e:
        print(f"   Status: ❌ Error: {str(e)[:50]}")
    
    print()

print("="*80)
print("✅ Tenant Database Creation Complete!")
print("="*80)

