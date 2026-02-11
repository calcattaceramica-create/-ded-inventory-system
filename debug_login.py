"""
Debug Login Process
تصحيح عملية تسجيل الدخول
"""
import sqlite3
import os
from pathlib import Path

# Paths
master_db = "C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db"
tenant_db = "C:/Users/DELL/Desktop/DED_Portable_App/tenant_C081D92695E08A84.db"

# Test credentials
license_key = "C081-D926-95E0-8A84"
username = "ABDO"
password = "123456"

print("=" * 80)
print("🔍 تصحيح عملية تسجيل الدخول - Debug Login Process")
print("=" * 80)
print()

print("📋 بيانات الاختبار:")
print(f"   License Key: {license_key}")
print(f"   Username: {username}")
print(f"   Password: {password}")
print()

# Step 1: Check Master Database
print("=" * 80)
print("1️⃣ فحص قاعدة البيانات الرئيسية (Master Database)")
print("=" * 80)

if not os.path.exists(master_db):
    print(f"❌ قاعدة البيانات الرئيسية غير موجودة: {master_db}")
else:
    print(f"✅ قاعدة البيانات الرئيسية موجودة")
    
    conn = sqlite3.connect(master_db)
    cursor = conn.cursor()
    
    # Check license
    cursor.execute("""
        SELECT license_key, client_name, admin_username, is_active, is_suspended, expires_at
        FROM licenses
        WHERE license_key = ?
    """, (license_key,))
    
    license = cursor.fetchone()
    
    if not license:
        print(f"❌ الترخيص غير موجود في قاعدة البيانات الرئيسية!")
        print()
        print("التراخيص الموجودة:")
        cursor.execute("SELECT license_key, client_name FROM licenses")
        all_licenses = cursor.fetchall()
        for lic in all_licenses:
            print(f"  - {lic[0]} ({lic[1]})")
    else:
        lic_key, client_name, admin_username, is_active, is_suspended, expires_at = license
        print(f"✅ الترخيص موجود!")
        print(f"   License Key: {lic_key}")
        print(f"   Client: {client_name}")
        print(f"   Admin Username: {admin_username}")
        print(f"   Active: {is_active}")
        print(f"   Suspended: {is_suspended}")
        print(f"   Expires: {expires_at}")
    
    conn.close()

print()

# Step 2: Check Tenant Database
print("=" * 80)
print("2️⃣ فحص قاعدة بيانات الترخيص (Tenant Database)")
print("=" * 80)

if not os.path.exists(tenant_db):
    print(f"❌ قاعدة بيانات الترخيص غير موجودة: {tenant_db}")
else:
    print(f"✅ قاعدة بيانات الترخيص موجودة")
    
    conn = sqlite3.connect(tenant_db)
    cursor = conn.cursor()
    
    # Check user
    cursor.execute("""
        SELECT id, username, email, is_active, is_admin
        FROM users
        WHERE username = ?
    """, (username,))
    
    user = cursor.fetchone()
    
    if not user:
        print(f"❌ المستخدم '{username}' غير موجود!")
        print()
        print("المستخدمون الموجودون:")
        cursor.execute("SELECT id, username, email FROM users")
        all_users = cursor.fetchall()
        for u in all_users:
            print(f"  - ID: {u[0]}, Username: {u[1]}, Email: {u[2]}")
    else:
        user_id, db_username, email, is_active, is_admin = user
        print(f"✅ المستخدم موجود!")
        print(f"   ID: {user_id}")
        print(f"   Username: {db_username}")
        print(f"   Email: {email}")
        print(f"   Active: {is_active}")
        print(f"   Admin: {is_admin}")
    
    conn.close()

print()

# Step 3: Summary
print("=" * 80)
print("📊 الخلاصة - Summary")
print("=" * 80)
print()
print("✅ يجب أن تعمل عملية تسجيل الدخول بالبيانات التالية:")
print()
print(f"   🔑 License Key: {license_key}")
print(f"   👤 Username: {username}")
print(f"   🔒 Password: {password}")
print()
print("=" * 80)

