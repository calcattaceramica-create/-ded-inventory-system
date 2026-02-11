import sqlite3

db_path = r"C:\Users\DELL\Desktop\DED_Portable_App\erp_system.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check admin user
cursor.execute("SELECT id, username, is_admin, role_id FROM users WHERE username = 'admin'")
admin = cursor.fetchone()
print(f"Admin user: ID={admin[0]}, is_admin={admin[2]}, role_id={admin[3]}")

# Check dashboard.view permission
cursor.execute("SELECT id, name FROM permissions WHERE name = 'dashboard.view'")
perm = cursor.fetchone()
if perm:
    print(f"\nPermission 'dashboard.view': ID={perm[0]}")
    
    # Check if role has this permission
    cursor.execute("""
        SELECT rp.id FROM role_permissions rp
        WHERE rp.role_id = ? AND rp.permission_id = ?
    """, (admin[3], perm[0]))
    
    role_perm = cursor.fetchone()
    if role_perm:
        print(f"✅ Role {admin[3]} HAS permission 'dashboard.view'")
    else:
        print(f"❌ Role {admin[3]} does NOT have permission 'dashboard.view'")
        print("Adding it now...")
        cursor.execute("""
            INSERT INTO role_permissions (role_id, permission_id)
            VALUES (?, ?)
        """, (admin[3], perm[0]))
        conn.commit()
        print("✅ Permission added!")
else:
    print("\n❌ Permission 'dashboard.view' does NOT exist!")

conn.close()
print("\nDone!")

