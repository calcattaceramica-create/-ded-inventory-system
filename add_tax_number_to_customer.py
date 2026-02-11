import sqlite3

# Connect to database
conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/tenant_C081_D926_95E0_8A84.db')
cursor = conn.cursor()

# Get first customer
cursor.execute('SELECT id, name, code FROM customers LIMIT 1')
customer = cursor.fetchone()

if customer:
    customer_id = customer[0]
    customer_name = customer[1]
    customer_code = customer[2]
    
    # Add tax number
    tax_number = '123456789012345'  # رقم ضريبي تجريبي
    
    cursor.execute('UPDATE customers SET tax_number = ? WHERE id = ?', (tax_number, customer_id))
    conn.commit()
    
    print(f'✅ تم إضافة الرقم الضريبي للعميل:')
    print(f'   ID: {customer_id}')
    print(f'   Name: {customer_name}')
    print(f'   Code: {customer_code}')
    print(f'   Tax Number: {tax_number}')
    
    # Verify
    cursor.execute('SELECT tax_number FROM customers WHERE id = ?', (customer_id,))
    result = cursor.fetchone()
    print(f'\n✅ التحقق: الرقم الضريبي المحفوظ = {result[0]}')
else:
    print('❌ لا يوجد عملاء في قاعدة البيانات')

conn.close()

