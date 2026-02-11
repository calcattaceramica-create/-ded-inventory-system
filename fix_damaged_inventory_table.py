"""
إنشاء جدول المخزون التالف - Create damaged_inventory table
"""
import sqlite3
import os

print("=" * 80)
print("🔧 إنشاء جدول المخزون التالف")
print("🔧 Creating damaged_inventory table")
print("=" * 80)

# Database path
db_path = r"C:\Users\DELL\DED\erp_system.db"

if not os.path.exists(db_path):
    print(f"\n❌ قاعدة البيانات غير موجودة: {db_path}")
    print("جرب المسار الآخر...")
    db_path = r"C:\Users\DELL\Desktop\DED_Portable_App\erp_system.db"
    
if not os.path.exists(db_path):
    print(f"\n❌ قاعدة البيانات غير موجودة: {db_path}")
    exit(1)

print(f"\n📂 قاعدة البيانات: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='damaged_inventory'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print("\n⚠️  جدول damaged_inventory موجود بالفعل")
        print("هل تريد حذفه وإعادة إنشائه؟ (y/n)")
        # For automation, we'll just show the structure
        cursor.execute("PRAGMA table_info(damaged_inventory)")
        columns = cursor.fetchall()
        print("\n📊 الأعمدة الحالية:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
    else:
        print("\n📝 إنشاء جدول damaged_inventory...")
        
        # Create damaged_inventory table
        cursor.execute("""
            CREATE TABLE damaged_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                warehouse_id INTEGER NOT NULL,
                quantity FLOAT NOT NULL DEFAULT 0,
                reason TEXT,
                damage_type VARCHAR(50),
                cost_value FLOAT DEFAULT 0,
                notes TEXT,
                user_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id),
                FOREIGN KEY (warehouse_id) REFERENCES warehouses (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        print("✅ تم إنشاء جدول damaged_inventory بنجاح!")
        
        # Verify the table
        cursor.execute("PRAGMA table_info(damaged_inventory)")
        columns = cursor.fetchall()
        
        print("\n📊 الأعمدة المنشأة:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ تم إصلاح جدول المخزون التالف بنجاح!")
    print("✅ Damaged inventory table fixed successfully!")
    print("=" * 80)
    
    print("\n📋 الخطوات التالية:")
    print("1. أعد تشغيل التطبيق")
    print("2. جرب الدخول إلى صفحة المخزون التالف")
    print("3. URL: http://127.0.0.1:5000/inventory/damaged-inventory")
    
except Exception as e:
    print(f"\n❌ خطأ: {str(e)}")
    import traceback
    traceback.print_exc()

