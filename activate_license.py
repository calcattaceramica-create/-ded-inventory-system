"""
Activate License
تفعيل الترخيص
"""
import sqlite3

# Database path
master_db = "C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db"

# License to activate
license_key = "C081-D926-95E0-8A84"

print("=" * 80)
print("🔧 تفعيل الترخيص - Activate License")
print("=" * 80)
print()

try:
    # Connect to master database
    conn = sqlite3.connect(master_db)
    cursor = conn.cursor()
    
    # Check current status
    cursor.execute("""
        SELECT license_key, is_active, is_suspended, suspension_reason
        FROM licenses
        WHERE license_key = ?
    """, (license_key,))
    
    license = cursor.fetchone()
    
    if not license:
        print(f"❌ الترخيص غير موجود: {license_key}")
    else:
        lic_key, is_active, is_suspended, suspension_reason = license
        
        print(f"📋 الحالة الحالية:")
        print(f"   License Key: {lic_key}")
        print(f"   Active: {is_active}")
        print(f"   Suspended: {is_suspended}")
        print(f"   Suspension Reason: {suspension_reason}")
        print()
        
        # Activate license
        cursor.execute("""
            UPDATE licenses
            SET is_active = 1, is_suspended = 0, suspension_reason = NULL
            WHERE license_key = ?
        """, (license_key,))
        
        conn.commit()
        
        print(f"✅ تم تفعيل الترخيص بنجاح!")
        print()
        
        # Verify
        cursor.execute("""
            SELECT license_key, is_active, is_suspended
            FROM licenses
            WHERE license_key = ?
        """, (license_key,))
        
        updated_license = cursor.fetchone()
        lic_key, is_active, is_suspended = updated_license
        
        print(f"📋 الحالة الجديدة:")
        print(f"   License Key: {lic_key}")
        print(f"   Active: {is_active}")
        print(f"   Suspended: {is_suspended}")
    
    conn.close()
    
    print()
    print("=" * 80)
    print("🎉 العملية اكتملت بنجاح!")
    print("=" * 80)
    print()
    print("الآن يمكنك تسجيل الدخول باستخدام:")
    print(f"   License Key: {license_key}")
    print(f"   Username: ABDO")
    print(f"   Password: 123456")
    
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()

