"""
Update Users Table Structure
تحديث بنية جدول المستخدمين لإضافة role_id و branch_id و license_id
"""
import sqlite3
import os
from pathlib import Path

def update_users_table(db_path):
    """Update users table to add missing columns"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get current columns
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add role_id if not exists
        if 'role_id' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN role_id INTEGER")
            print(f"  ✅ Added role_id column")
        
        # Add branch_id if not exists
        if 'branch_id' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN branch_id INTEGER")
            print(f"  ✅ Added branch_id column")
        
        # Add license_id if not exists
        if 'license_id' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN license_id INTEGER")
            print(f"  ✅ Added license_id column")
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("=" * 80)
    print("🔧 تحديث بنية جدول المستخدمين - Updating Users Table Structure")
    print("=" * 80)
    print()
    
    # Desktop path
    desktop_path = Path("C:/Users/DELL/Desktop/DED_Portable_App")
    
    # Find all tenant databases
    tenant_dbs = list(desktop_path.glob("tenant_*.db"))
    
    print(f"📂 Found {len(tenant_dbs)} tenant databases")
    print()
    
    success_count = 0
    for db_path in tenant_dbs:
        db_name = db_path.name
        print(f"🔄 Processing: {db_name}")
        
        if update_users_table(str(db_path)):
            success_count += 1
            print(f"  ✅ Updated successfully")
        else:
            print(f"  ❌ Failed to update")
        print()
    
    print("=" * 80)
    print(f"🎉 تم تحديث {success_count} من {len(tenant_dbs)} قاعدة بيانات بنجاح!")
    print("=" * 80)

if __name__ == "__main__":
    main()

