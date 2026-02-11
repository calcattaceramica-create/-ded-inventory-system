"""
Fix Stocks Table - Add missing columns
إصلاح جدول المخزون - إضافة الأعمدة المفقودة
"""

import sqlite3
import os

def fix_stocks_table():
    """Add missing columns to stocks table"""
    
    db_path = "C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db"
    
    print("=" * 70)
    print("🔧 Fixing Stocks Table")
    print("=" * 70)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current columns
        cursor.execute("PRAGMA table_info(stocks)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"\n📊 Current columns in stocks table:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        # List of columns that should exist
        required_columns = {
            'damaged_quantity': 'FLOAT DEFAULT 0',
            'reserved_quantity': 'FLOAT DEFAULT 0',
            'available_quantity': 'FLOAT DEFAULT 0',
            'last_updated': 'DATETIME'
        }
        
        # Add missing columns
        added_columns = []
        for col_name, col_type in required_columns.items():
            if col_name not in column_names:
                print(f"\n⚠️  Column '{col_name}' not found. Adding it...")
                cursor.execute(f"""
                    ALTER TABLE stocks 
                    ADD COLUMN {col_name} {col_type}
                """)
                added_columns.append(col_name)
                print(f"✅ Column '{col_name}' added successfully!")
        
        if not added_columns:
            print(f"\n✅ All required columns already exist!")
        else:
            conn.commit()
            print(f"\n✅ Added {len(added_columns)} column(s): {', '.join(added_columns)}")
        
        # Update available_quantity for existing records
        print(f"\n🔄 Updating available_quantity for existing records...")
        cursor.execute("""
            UPDATE stocks 
            SET available_quantity = quantity - COALESCE(reserved_quantity, 0) - COALESCE(damaged_quantity, 0)
            WHERE available_quantity IS NULL OR available_quantity = 0
        """)
        updated_rows = cursor.rowcount
        conn.commit()
        print(f"✅ Updated {updated_rows} record(s)")
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(stocks)")
        columns = cursor.fetchall()
        
        print(f"\n📊 Updated columns in stocks table:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ Stocks table fixed successfully!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_stocks_table()

