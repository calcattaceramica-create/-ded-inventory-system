"""
إنشاء الملفات المفقودة لنظام التراخيص
Create missing files for license system
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
from werkzeug.security import generate_password_hash

print("=" * 80)
print("📝 إنشاء الملفات المفقودة لنظام التراخيص")
print("📝 Creating missing files for license system")
print("=" * 80)
print()

base_path = Path(r"C:\Users\DELL\Desktop\DED_Portable_App")

# Step 1: Create licenses.json with existing licenses
print("📄 الخطوة 1: إنشاء licenses.json...")
print()

licenses_json = {
    "CEC9-79EE-C42F-2DAD": {
        "company": "DED ERP System",
        "expiry": "2027-07-05",
        "created": "2025-01-12 10:30:00",
        "duration_days": 900,
        "machine_id": "DESKTOP-MAIN",
        "license_type": "Standard",
        "max_users": 50,
        "features": ["all"],
        "status": "active",
        "activation_count": 0,
        "last_check": None,
        "username": "admin",
        "password": "admin123",
        "contact_email": "admin@ded-erp.com",
        "contact_phone": "",
        "notes": "Main DED ERP License"
    },
    "6356-6964-93AE-B60D": {
        "company": "Test Client 1",
        "expiry": "2026-02-19",
        "created": "2025-01-20 14:00:00",
        "duration_days": 365,
        "machine_id": "TEST-MACHINE-1",
        "license_type": "Standard",
        "max_users": 10,
        "features": ["all"],
        "status": "active",
        "activation_count": 0,
        "last_check": None,
        "username": "admin",
        "password": "admin123",
        "contact_email": "test1@example.com",
        "contact_phone": "",
        "notes": "Test License 1"
    },
    "F730-BD34-0A48-A98B": {
        "company": "Test Client 2",
        "expiry": "2026-02-19",
        "created": "2025-01-20 14:05:00",
        "duration_days": 365,
        "machine_id": "TEST-MACHINE-2",
        "license_type": "Standard",
        "max_users": 10,
        "features": ["all"],
        "status": "active",
        "activation_count": 0,
        "last_check": None,
        "username": "admin",
        "password": "admin123",
        "contact_email": "test2@example.com",
        "contact_phone": "",
        "notes": "Test License 2"
    }
}

licenses_path = base_path / "licenses.json"
try:
    with open(licenses_path, 'w', encoding='utf-8') as f:
        json.dump(licenses_json, f, ensure_ascii=False, indent=4)
    print(f"   ✅ تم إنشاء licenses.json مع {len(licenses_json)} تراخيص")
except Exception as e:
    print(f"   ❌ خطأ في إنشاء licenses.json: {e}")

print()

# Step 2: Create licenses_master.db
print("📄 الخطوة 2: إنشاء licenses_master.db...")
print()

db_path = base_path / "licenses_master.db"
try:
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create licenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_key TEXT UNIQUE NOT NULL,
            license_hash TEXT,
            client_name TEXT,
            client_company TEXT,
            client_email TEXT,
            client_phone TEXT,
            machine_id TEXT,
            expires_at DATETIME,
            license_type TEXT DEFAULT 'Standard',
            max_users INTEGER DEFAULT 10,
            max_branches INTEGER DEFAULT 5,
            is_active BOOLEAN DEFAULT 1,
            is_suspended BOOLEAN DEFAULT 0,
            suspension_reason TEXT,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            activated_at DATETIME,
            admin_username TEXT,
            admin_password_hash TEXT
        )
    ''')
    
    # Insert licenses
    for key, data in licenses_json.items():
        license_hash = hashlib.sha256(key.encode()).hexdigest()
        admin_password_hash = generate_password_hash(data['password'])
        expiry_date = datetime.strptime(data['expiry'], "%Y-%m-%d")
        
        cursor.execute('''
            INSERT OR REPLACE INTO licenses (
                license_key, license_hash, client_name, client_company,
                client_email, client_phone, machine_id, expires_at,
                license_type, max_users, max_branches, is_active,
                is_suspended, notes, created_at, admin_username, admin_password_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            key,
            license_hash,
            data['username'],
            data['company'],
            data.get('contact_email', ''),
            data.get('contact_phone', ''),
            data['machine_id'],
            expiry_date,
            data['license_type'],
            data['max_users'],
            5,
            1 if data['status'] == 'active' else 0,
            0,
            data.get('notes', ''),
            data['created'],
            data['username'],
            admin_password_hash
        ))
    
    conn.commit()
    conn.close()
    
    print(f"   ✅ تم إنشاء licenses_master.db مع {len(licenses_json)} تراخيص")
except Exception as e:
    print(f"   ❌ خطأ في إنشاء licenses_master.db: {e}")

print()
print("=" * 80)
print("✅ تم إنشاء جميع الملفات المفقودة!")
print("=" * 80)
print()
print("📋 الملفات المنشأة:")
print(f"   ✅ {licenses_path}")
print(f"   ✅ {db_path}")
print()
print("🎯 الآن يمكنك:")
print("   1. تشغيل DED_Control_Panel.pyw من سطح المكتب")
print("   2. تسجيل الدخول بأحد التراخيص:")
print("      - License: CEC9-79EE-C42F-2DAD")
print("      - Username: admin")
print("      - Password: admin123")
print()

