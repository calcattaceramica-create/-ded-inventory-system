import sqlite3

# Connect to database
conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/tenant_C081-D926-95E0-8A84.db')
cursor = conn.cursor()

# Get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print('=== الجداول ===')
for t in tables:
    print(t[0])

conn.close()

