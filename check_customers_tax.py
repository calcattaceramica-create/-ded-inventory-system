import sqlite3

# Connect to database
conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/tenant_C081-D926-95E0-8A84.db')
cursor = conn.cursor()

# Get customers
cursor.execute('SELECT id, name, code, tax_number FROM customers LIMIT 10')
customers = cursor.fetchall()

print('=== العملاء ===')
for c in customers:
    tax_num = c[3] if c[3] else 'لا يوجد'
    print(f'ID: {c[0]}, Name: {c[1]}, Code: {c[2]}, Tax Number: {tax_num}')

conn.close()

