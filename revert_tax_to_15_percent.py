"""
إرجاع معدل الضريبة من 18% إلى 15% في جميع الملفات
Revert tax rate from 18% to 15% in all files
"""
import os
import re

print("=" * 80)
print("🔄 إرجاع معدل الضريبة من 18% إلى 15%")
print("🔄 Reverting tax rate from 18% to 15%")
print("=" * 80)

# File paths
base_path = r"C:\Users\DELL\DED"
files_to_fix = [
    {
        'path': os.path.join(base_path, 'models.py'),
        'changes': [
            {
                'old': '    tax_rate = db.Column(db.Float, default=18.0)',
                'new': '    tax_rate = db.Column(db.Float, default=15.0)',
                'description': 'Company model tax_rate default'
            }
        ]
    },
    {
        'path': os.path.join(base_path, 'add_invoice.html'),
        'changes': [
            {
                'old': "{{ _('Tax (18%)') }}",
                'new': "{{ _('Tax (15%)') }}",
                'description': 'Invoice template tax label'
            },
            {
                'old': 'const taxRate = option && option.value ? (parseFloat(option.getAttribute(\'data-tax\')) || 18) : 18;',
                'new': 'const taxRate = option && option.value ? (parseFloat(option.getAttribute(\'data-tax\')) || 15) : 15;',
                'description': 'JavaScript tax calculation'
            }
        ]
    }
]

# Process each file
for file_info in files_to_fix:
    file_path = file_info['path']
    
    if not os.path.exists(file_path):
        print(f"\n⚠️  الملف غير موجود: {file_path}")
        continue
    
    print(f"\n📝 معالجة الملف: {os.path.basename(file_path)}")
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # Apply changes
    for change in file_info['changes']:
        if change['old'] in content:
            content = content.replace(change['old'], change['new'])
            changes_made += 1
            print(f"   ✅ {change['description']}")
        else:
            print(f"   ⚠️  لم يتم العثور على: {change['description']}")
    
    # Write back if changes were made
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   💾 تم حفظ {changes_made} تغيير(ات)")
    else:
        print(f"   ℹ️  لا توجد تغييرات")

print("\n" + "=" * 80)
print("✅ تم إرجاع معدل الضريبة إلى 15% بنجاح!")
print("✅ Tax rate successfully reverted to 15%!")
print("=" * 80)

print("\n📋 الخطوات التالية:")
print("1. أعد تشغيل التطبيق")
print("2. تحقق من فواتير المبيعات والمشتريات")
print("3. تأكد من أن الضريبة 15% في جميع الفواتير الجديدة")

