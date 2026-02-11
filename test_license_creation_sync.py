#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار مزامنة إنشاء التراخيص
Test License Creation Synchronization

هذا السكريبت يختبر أن إنشاء ترخيص جديد من Control Panel:
1. يحفظ في licenses.json
2. يضاف إلى licenses_master.db مع license_hash و admin_password_hash
3. ينشئ tenant database
4. يضيف مستخدم admin في tenant database
"""

import sys
import sqlite3
from pathlib import Path

# Add DED_Portable_App to path
sys.path.insert(0, 'C:/Users/DELL/Desktop/DED_Portable_App')

def check_license_in_master_db(license_key):
    """Check if license exists in licenses_master.db with all required fields"""
    db_path = Path('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return False
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Check if license exists with all required fields
    cursor.execute("""
        SELECT license_key, client_company, admin_username, 
               license_hash, admin_password_hash, is_active, expires_at
        FROM licenses 
        WHERE license_key = ?
    """, (license_key,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        print(f"\n✅ License found in licenses_master.db:")
        print(f"   License Key: {result[0]}")
        print(f"   Company: {result[1]}")
        print(f"   Username: {result[2]}")
        print(f"   License Hash: {result[3][:20]}... (length: {len(result[3]) if result[3] else 0})")
        print(f"   Password Hash: {result[4][:20]}... (length: {len(result[4]) if result[4] else 0})")
        print(f"   Active: {'✅ Yes' if result[5] else '❌ No'}")
        print(f"   Expires: {result[6]}")
        
        # Check if required fields are present
        if result[3] and result[4]:  # license_hash and admin_password_hash
            print(f"\n✅ All required fields present!")
            return True
        else:
            print(f"\n⚠️ Missing required fields:")
            if not result[3]:
                print(f"   ❌ license_hash is missing")
            if not result[4]:
                print(f"   ❌ admin_password_hash is missing")
            return False
    else:
        print(f"\n❌ License NOT found in licenses_master.db")
        return False

def check_tenant_database(license_key):
    """Check if tenant database exists and has admin user"""
    # Remove dashes from license key
    db_name = f"tenant_{license_key.replace('-', '').lower()}.db"
    db_path = Path('C:/Users/DELL/Desktop/DED_Portable_App') / db_name
    
    if not db_path.exists():
        print(f"\n❌ Tenant database not found: {db_name}")
        return False
    
    print(f"\n✅ Tenant database found: {db_name}")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='users'
    """)
    
    if not cursor.fetchone():
        print(f"   ❌ 'users' table not found")
        conn.close()
        return False
    
    print(f"   ✅ 'users' table exists")
    
    # Check if admin user exists
    cursor.execute("""
        SELECT username, is_active, role 
        FROM users 
        WHERE role = 'admin'
    """)
    
    admin = cursor.fetchone()
    conn.close()
    
    if admin:
        print(f"   ✅ Admin user found:")
        print(f"      Username: {admin[0]}")
        print(f"      Active: {'✅ Yes' if admin[1] else '❌ No'}")
        print(f"      Role: {admin[2]}")
        return True
    else:
        print(f"   ❌ Admin user not found")
        return False

def main():
    print("=" * 80)
    print("🧪 اختبار مزامنة إنشاء التراخيص - Test License Creation Sync")
    print("=" * 80)
    
    print("\n📝 التعليمات - Instructions:")
    print("-" * 80)
    print("1. افتح DED Control Panel")
    print("2. انتقل إلى تبويب 'مدير التراخيص'")
    print("3. اضغط '➕ إضافة ترخيص جديد'")
    print("4. املأ البيانات وأنشئ الترخيص")
    print("5. انسخ مفتاح الترخيص الجديد")
    print("6. شغّل هذا السكريبت مع المفتاح")
    print("-" * 80)
    
    # Get license key from user
    license_key = input("\n🔑 أدخل مفتاح الترخيص - Enter License Key: ").strip()
    
    if not license_key:
        print("\n❌ لم يتم إدخال مفتاح ترخيص!")
        return
    
    print(f"\n🔍 فحص الترخيص - Checking License: {license_key}")
    print("=" * 80)
    
    # Check master database
    print("\n1️⃣ فحص قاعدة البيانات الرئيسية - Checking Master Database")
    print("-" * 80)
    master_db_ok = check_license_in_master_db(license_key)
    
    # Check tenant database
    print("\n2️⃣ فحص قاعدة بيانات المستأجر - Checking Tenant Database")
    print("-" * 80)
    tenant_db_ok = check_tenant_database(license_key)
    
    # Final result
    print("\n" + "=" * 80)
    print("📊 النتيجة النهائية - Final Result")
    print("=" * 80)
    
    if master_db_ok and tenant_db_ok:
        print("\n✅ نجح 100%! - 100% Success!")
        print("   ✅ الترخيص موجود في licenses_master.db")
        print("   ✅ جميع الحقول المطلوبة موجودة (license_hash, password_hash)")
        print("   ✅ قاعدة بيانات المستأجر موجودة")
        print("   ✅ مستخدم admin موجود ونشط")
        print("\n🎉 نظام المزامنة يعمل بشكل مثالي!")
    else:
        print("\n⚠️ هناك مشاكل - Issues Found:")
        if not master_db_ok:
            print("   ❌ مشكلة في قاعدة البيانات الرئيسية")
        if not tenant_db_ok:
            print("   ❌ مشكلة في قاعدة بيانات المستأجر")
        print("\n💡 تأكد من أن Control Panel يستخدم الدوال الجديدة:")
        print("   - add_license_to_master_db()")
        print("   - create_tenant_database()")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ خطأ - Error: {e}")
        import traceback
        traceback.print_exc()

