import sqlite3

db_path = r"C:\Users\DELL\Desktop\DED_Portable_App\erp_system.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check admin user
cursor.execute("SELECT id, username, is_admin, role_id FROM users WHERE username = 'admin'")
admin = cursor.fetchone()
print(f"Admin user: ID={admin[0]}, username={admin[1]}, is_admin={admin[2]}, role_id={admin[3]}")

# Check if permission exists
cursor.execute("SELECT id, name, name_ar FROM permissions WHERE name = 'inventory.stock.view'")
perm = cursor.fetchone()
if perm:
    print(f"\nPermission exists: ID={perm[0]}, name={perm[1]}, name_ar={perm[2]}")
else:
    print("\n⚠️ Permission 'inventory.stock.view' does NOT exist!")
    print("Creating it...")
    cursor.execute("""
        INSERT INTO permissions (name, name_ar, module)
        VALUES ('inventory.stock.view', 'عرض المخزون', 'inventory')
    """)
    conn.commit()
    print("✅ Permission created!")

conn.close()
print("\nDone!")

