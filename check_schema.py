import sqlite3
from pathlib import Path

db_path = Path('C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db')
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get table schema
cursor.execute("PRAGMA table_info(licenses)")
columns = cursor.fetchall()

print("Licenses table schema:")
print("="*60)
for col in columns:
    print(f"{col[1]} ({col[2]})")

conn.close()

