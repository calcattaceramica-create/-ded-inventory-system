import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('C:/Users/DELL/Desktop/DED_Portable_App/tenant_C081_D926_95E0_8A84.db')
cursor = conn.cursor()

# Check if customers table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
if not cursor.fetchone():
    print('❌ جدول customers غير موجود')
    conn.close()
    exit()

# Create a test customer with tax number
customer_data = {
    'code': 'CUST001',
    'name': 'شركة الاختبار المحدودة',
    'name_en': 'Test Company Ltd',
    'email': 'test@company.com',
    'phone': '0501234567',
    'mobile': '0501234567',
    'address': 'الرياض، المملكة العربية السعودية',
    'city': 'الرياض',
    'country': 'السعودية',
    'tax_number': '300123456789003',  # رقم ضريبي سعودي تجريبي
    'commercial_register': 'CR123456',
    'customer_type': 'company',
    'credit_limit': 50000.00,
    'current_balance': 0.00,
    'payment_terms': 30,
    'category': 'A',
    'rating': 5,
    'is_active': 1,
    'notes': 'عميل تجريبي لاختبار الرقم الضريبي',
    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

try:
    cursor.execute('''
        INSERT INTO customers (
            code, name, name_en, email, phone, mobile, address, city, country,
            tax_number, commercial_register, customer_type, credit_limit, current_balance,
            payment_terms, category, rating, is_active, notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        customer_data['code'], customer_data['name'], customer_data['name_en'],
        customer_data['email'], customer_data['phone'], customer_data['mobile'],
        customer_data['address'], customer_data['city'], customer_data['country'],
        customer_data['tax_number'], customer_data['commercial_register'],
        customer_data['customer_type'], customer_data['credit_limit'],
        customer_data['current_balance'], customer_data['payment_terms'],
        customer_data['category'], customer_data['rating'], customer_data['is_active'],
        customer_data['notes'], customer_data['created_at'], customer_data['updated_at']
    ))
    
    conn.commit()
    
    # Get the created customer
    cursor.execute('SELECT id, name, code, tax_number FROM customers WHERE code = ?', (customer_data['code'],))
    customer = cursor.fetchone()
    
    print('✅ تم إنشاء عميل جديد بنجاح:')
    print(f'   ID: {customer[0]}')
    print(f'   Name: {customer[1]}')
    print(f'   Code: {customer[2]}')
    print(f'   Tax Number: {customer[3]}')
    print('\n📋 يمكنك الآن إنشاء فاتورة لهذا العميل لرؤية الرقم الضريبي!')
    
except sqlite3.IntegrityError as e:
    print(f'❌ خطأ: العميل موجود بالفعل أو هناك مشكلة في البيانات: {e}')
except Exception as e:
    print(f'❌ خطأ: {e}')

conn.close()

