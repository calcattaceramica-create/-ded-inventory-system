"""
Simple License Manager
مدير تراخيص بسيط للتحكم من الخارج
"""
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')

class LicenseManager:
    """License Manager Class"""
    
    @staticmethod
    def get_connection():
        """Get database connection"""
        return sqlite3.connect(str(DB_PATH))
    
    @staticmethod
    def get_all_licenses():
        """Get all licenses"""
        conn = LicenseManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_key, client_name, client_company, admin_username,
                   is_active, is_suspended, suspension_reason, expires_at, created_at
            FROM licenses
            ORDER BY created_at DESC
        ''')
        
        licenses = cursor.fetchall()
        conn.close()
        return licenses
    
    @staticmethod
    def activate_license(license_key):
        """Activate a license"""
        conn = LicenseManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE licenses
            SET is_active = 1, is_suspended = 0, suspension_reason = NULL
            WHERE license_key = ?
        ''', (license_key,))
        
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    @staticmethod
    def suspend_license(license_key, reason="تم الإيقاف من لوحة التحكم"):
        """Suspend a license"""
        conn = LicenseManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE licenses
            SET is_suspended = 1, suspension_reason = ?
            WHERE license_key = ?
        ''', (reason, license_key))
        
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    @staticmethod
    def deactivate_license(license_key):
        """Deactivate a license"""
        conn = LicenseManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE licenses
            SET is_active = 0
            WHERE license_key = ?
        ''', (license_key,))
        
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    @staticmethod
    def extend_license(license_key, days=30):
        """Extend license expiration"""
        conn = LicenseManager.get_connection()
        cursor = conn.cursor()
        
        # Get current expiration
        cursor.execute('SELECT expires_at FROM licenses WHERE license_key = ?', (license_key,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False, "الترخيص غير موجود"
        
        current_expires = row[0]
        
        # Parse current expiration
        if current_expires:
            try:
                expires_dt = datetime.strptime(current_expires, '%Y-%m-%d %H:%M:%S')
            except:
                expires_dt = datetime.now()
        else:
            expires_dt = datetime.now()
        
        # Add days
        new_expires = expires_dt + timedelta(days=days)
        
        cursor.execute('''
            UPDATE licenses
            SET expires_at = ?
            WHERE license_key = ?
        ''', (new_expires.strftime('%Y-%m-%d %H:%M:%S'), license_key))
        
        conn.commit()
        conn.close()
        
        return True, new_expires.strftime('%Y-%m-%d %H:%M:%S')

# Test functions
if __name__ == '__main__':
    print("="*80)
    print("🔧 License Manager Test")
    print("="*80)
    print()
    
    # Get all licenses
    print("📋 All Licenses:")
    print("-"*80)
    licenses = LicenseManager.get_all_licenses()
    
    for i, lic in enumerate(licenses, 1):
        print(f"{i}. {lic[0]}")
        print(f"   Client: {lic[1]}")
        print(f"   Username: {lic[3]}")
        print(f"   Active: {'✅' if lic[4] else '❌'}")
        print(f"   Suspended: {'⚠️ Yes' if lic[5] else '✅ No'}")
        if lic[6]:
            print(f"   Reason: {lic[6]}")
        print(f"   Expires: {lic[7]}")
        print()
    
    if licenses:
        test_license = licenses[0][0]
        
        print(f"🧪 Testing with license: {test_license}")
        print()
        
        # Test suspend
        print("⏸️ Suspending license...")
        if LicenseManager.suspend_license(test_license, "Test suspension"):
            print("✅ License suspended!")
        
        # Test activate
        print("▶️ Activating license...")
        if LicenseManager.activate_license(test_license):
            print("✅ License activated!")
        
        # Test extend
        print("📅 Extending license by 60 days...")
        success, result = LicenseManager.extend_license(test_license, 60)
        if success:
            print(f"✅ License extended! New expiration: {result}")
    
    print()
    print("="*80)
    print("✅ Test Complete!")
    print("="*80)

