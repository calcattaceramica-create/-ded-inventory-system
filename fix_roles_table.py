"""
Fix Roles Table - Add description_en column
إصلاح جدول الأدوار - إضافة عمود description_en
"""

import sqlite3
import os

def fix_roles_table():
    """Add description_en column to roles table"""
    
    db_path = "C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db"
    
    print("=" * 70)
    print("🔧 Fixing Roles Table")
    print("=" * 70)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(roles)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"\n📊 Current columns in roles table:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        if 'description_en' not in column_names:
            print(f"\n⚠️  Column 'description_en' not found. Adding it...")
            
            # Add the missing column
            cursor.execute("""
                ALTER TABLE roles 
                ADD COLUMN description_en VARCHAR(256)
            """)
            conn.commit()
            
            print("✅ Column 'description_en' added successfully!")
        else:
            print(f"\n✅ Column 'description_en' already exists!")
        
        # Verify the change
        cursor.execute("PRAGMA table_info(roles)")
        columns = cursor.fetchall()
        
        print(f"\n📊 Updated columns in roles table:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ Roles table fixed successfully!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_roles_table()

