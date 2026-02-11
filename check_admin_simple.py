import sqlite3

db_path = r"C:\Users\DELL\Desktop\DED_Portable_App\erp_system.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check admin user
cursor.execute("SELECT id, username, is_admin FROM users WHERE username = 'admin'")
admin = cursor.fetchone()
print(f"Admin user: {admin}")

# Update to admin
cursor.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
conn.commit()

# Verify
cursor.execute("SELECT id, username, is_admin FROM users WHERE username = 'admin'")
admin = cursor.fetchone()
print(f"Updated admin user: {admin}")

conn.close()
print("Done!")

