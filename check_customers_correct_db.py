import sqlite3

# Try different database names
db_names = [
    'C:/Users/DELL/Desktop/DED_Portable_App/tenant_C081_D926_95E0_8A84.db',
    'C:/Users/DELL/Desktop/DED_Portable_App/tenant_c081d92695e08a84.db',
]

for db_name in db_names:
    try:
        print(f'\n=== Checking {db_name} ===')
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Check if customers table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
        if cursor.fetchone():
            print('✅ جدول customers موجود')
            
            # Get customers with tax numbers
            cursor.execute('SELECT id, name, code, tax_number FROM customers WHERE tax_number IS NOT NULL AND tax_number != "" LIMIT 5')
            customers = cursor.fetchall()
            
            if customers:
                print(f'✅ وجدت {len(customers)} عملاء لديهم رقم ضريبي:')
                for c in customers:
                    print(f'  - ID: {c[0]}, Name: {c[1]}, Code: {c[2]}, Tax Number: {c[3]}')
            else:
                print('⚠️ لا يوجد عملاء لديهم رقم ضريبي')
                
                # Get all customers
                cursor.execute('SELECT id, name, code FROM customers LIMIT 5')
                all_customers = cursor.fetchall()
                if all_customers:
                    print(f'📋 عينة من العملاء ({len(all_customers)}):')
                    for c in all_customers:
                        print(f'  - ID: {c[0]}, Name: {c[1]}, Code: {c[2]}')
        else:
            print('❌ جدول customers غير موجود')
        
        conn.close()
    except Exception as e:
        print(f'❌ خطأ: {e}')

