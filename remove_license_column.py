"""
Migration Script: Remove License System
إزالة نظام التراخيص من قاعدة البيانات

This script removes the license_id column from the users table
"""

import sqlite3
import os
from pathlib import Path

def remove_license_column_from_db(db_path):
    """Remove license_id column from users table"""
    print(f"\n🔧 Processing database: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"⚠️  Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if license_id column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'license_id' not in column_names:
            print(f"✅ license_id column does not exist in {db_path}")
            conn.close()
            return True
        
        print(f"📋 Found license_id column, removing it...")
        
        # Get all columns except license_id
        columns_to_keep = [col for col in columns if col[1] != 'license_id']
        column_defs = []
        for col in columns_to_keep:
            col_name = col[1]
            col_type = col[2]
            col_def = f"{col_name} {col_type}"
            
            # Add NOT NULL if needed
            if col[3] == 1:
                col_def += " NOT NULL"
            
            # Add DEFAULT if exists
            if col[4] is not None:
                col_def += f" DEFAULT {col[4]}"
            
            # Add PRIMARY KEY if needed
            if col[5] == 1:
                col_def += " PRIMARY KEY"
            
            column_defs.append(col_def)
        
        # Create new table without license_id
        create_table_sql = f"CREATE TABLE users_new ({', '.join(column_defs)})"
        cursor.execute(create_table_sql)
        
        # Copy data from old table to new table
        columns_str = ', '.join([col[1] for col in columns_to_keep])
        cursor.execute(f"INSERT INTO users_new ({columns_str}) SELECT {columns_str} FROM users")
        
        # Drop old table
        cursor.execute("DROP TABLE users")
        
        # Rename new table
        cursor.execute("ALTER TABLE users_new RENAME TO users")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Successfully removed license_id column from {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {db_path}: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def main():
    """Main migration function"""
    print("=" * 70)
    print("🔧 Migration: Remove License System")
    print("=" * 70)
    
    # Get the application directory
    app_dir = Path("C:/Users/DELL/Desktop/DED_Portable_App")
    
    if not app_dir.exists():
        print(f"❌ Application directory not found: {app_dir}")
        return
    
    # Find all database files
    db_files = []
    
    # Main database
    main_db = app_dir / "erp_system.db"
    if main_db.exists():
        db_files.append(main_db)
    
    # Tenant databases
    tenant_dbs = list(app_dir.glob("tenant_*.db"))
    db_files.extend(tenant_dbs)
    
    if not db_files:
        print("⚠️  No database files found")
        return
    
    print(f"\n📊 Found {len(db_files)} database file(s)")
    
    # Process each database
    success_count = 0
    for db_file in db_files:
        if remove_license_column_from_db(str(db_file)):
            success_count += 1
    
    print("\n" + "=" * 70)
    print(f"✅ Migration completed: {success_count}/{len(db_files)} databases updated")
    print("=" * 70)
    
    if success_count == len(db_files):
        print("\n🎉 All databases updated successfully!")
        print("📝 Next steps:")
        print("   1. Test login with username and password only")
        print("   2. Test user management (add/edit/delete)")
        print("   3. Verify no license-related errors appear")
    else:
        print(f"\n⚠️  {len(db_files) - success_count} database(s) failed to update")

if __name__ == "__main__":
    main()

