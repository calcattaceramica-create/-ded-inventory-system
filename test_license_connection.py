# -*- coding: utf-8 -*-
"""
Test License Connection Script
اختبار اتصال نظام التراخيص
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import secrets

def test_database_connection():
    """Test connection to the database"""
    db_path = Path("C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db")
    
    print("=" * 80)
    print("🔍 اختبار اتصال قاعدة البيانات - Testing Database Connection")
    print("=" * 80)
    print()
    
    # Check if database exists
    if not db_path.exists():
        print(f"❌ قاعدة البيانات غير موجودة - Database not found at:")
        print(f"   {db_path}")
        return False
    
    print(f"✅ قاعدة البيانات موجودة - Database found at:")
    print(f"   {db_path}")
    print()
    
    try:
        # Connect to database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📊 الجداول الموجودة - Available Tables:")
        for table in tables:
            print(f"   - {table[0]}")
        print()
        
        # Check licenses table structure
        if ('licenses',) in tables:
            cursor.execute("PRAGMA table_info(licenses)")
            columns = cursor.fetchall()
            
            print("🔑 هيكل جدول التراخيص - Licenses Table Structure:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")
            print()
            
            # Count licenses
            cursor.execute("SELECT COUNT(*) FROM licenses")
            count = cursor.fetchone()[0]
            print(f"📈 عدد التراخيص الموجودة - Total Licenses: {count}")
            print()
            
            # Show recent licenses
            if count > 0:
                cursor.execute("""
                    SELECT license_key, client_name, license_type, is_active, expires_at 
                    FROM licenses 
                    ORDER BY created_at DESC 
                    LIMIT 5
                """)
                licenses = cursor.fetchall()
                
                print("📋 آخر 5 تراخيص - Recent 5 Licenses:")
                for lic in licenses:
                    key = lic[0][:20] + "..." if lic[0] and len(lic[0]) > 20 else lic[0]
                    print(f"   - {key} | {lic[1]} | {lic[2]} | Active: {lic[3]} | Expires: {lic[4]}")
                print()
        
        # Check users table
        if ('users',) in tables:
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"👥 عدد المستخدمين - Total Users: {user_count}")
            
            if user_count > 0:
                cursor.execute("""
                    SELECT username, email, is_active, license_id 
                    FROM users 
                    LIMIT 5
                """)
                users = cursor.fetchall()
                
                print("👤 المستخدمون - Users:")
                for user in users:
                    print(f"   - {user[0]} | {user[1]} | Active: {user[2]} | License ID: {user[3]}")
                print()
        
        conn.close()
        
        print("=" * 80)
        print("✅ الاتصال ناجح - Connection Successful!")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"❌ خطأ - Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_database_connection()
    
    print()
    input("اضغط Enter للخروج - Press Enter to exit...")

