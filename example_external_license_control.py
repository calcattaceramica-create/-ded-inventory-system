#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مثال عملي: التحكم في التراخيص من خارج التطبيق
Example: External License Control

هذا السكريبت يوضح كيفية التحكم في التراخيص من خارج التطبيق الرئيسي
This script demonstrates how to control licenses externally
"""

import sys
from pathlib import Path

# Add DED_Portable_App to path
sys.path.insert(0, 'C:/Users/DELL/Desktop/DED_Portable_App')

from license_control import LicenseControl

def main():
    print("=" * 80)
    print("🔧 التحكم الخارجي في التراخيص - External License Control")
    print("=" * 80)
    
    # Initialize License Control
    lc = LicenseControl()
    
    # Get all licenses
    print("\n📋 جميع التراخيص - All Licenses:")
    print("-" * 80)
    licenses = lc.get_all_licenses()
    
    for i, lic in enumerate(licenses, 1):
        print(f"\n{i}. {lic['license_key']}")
        print(f"   الشركة - Company: {lic['client_company']}")
        print(f"   الحالة - Status: {'✅ Active' if lic['is_active'] else '❌ Inactive'}")
        print(f"   موقوف - Suspended: {'⚠️ Yes' if lic['is_suspended'] else '✓ No'}")
        print(f"   ينتهي - Expires: {lic['expires_at']}")
    
    # Example operations
    print("\n" + "=" * 80)
    print("💡 أمثلة على العمليات - Example Operations")
    print("=" * 80)
    
    # Choose a license for demonstration
    if licenses:
        demo_license = licenses[0]['license_key']
        print(f"\n🎯 سنستخدم الترخيص - Using license: {demo_license}")
        
        # Example 1: Suspend license
        print("\n" + "-" * 80)
        print("مثال 1: إيقاف ترخيص - Example 1: Suspend License")
        print("-" * 80)
        print(f"الكود - Code:")
        print(f'  lc.suspend_license("{demo_license}", "سبب الإيقاف")')
        print(f"\nلتنفيذ هذا المثال، قم بإلغاء التعليق عن السطر التالي:")
        print(f"# success, msg = lc.suspend_license('{demo_license}', 'اختبار الإيقاف')")
        print(f"# print(msg)")
        
        # Example 2: Activate license
        print("\n" + "-" * 80)
        print("مثال 2: تفعيل ترخيص - Example 2: Activate License")
        print("-" * 80)
        print(f"الكود - Code:")
        print(f'  lc.activate_license("{demo_license}")')
        print(f"\nلتنفيذ هذا المثال، قم بإلغاء التعليق عن السطر التالي:")
        print(f"# success, msg = lc.activate_license('{demo_license}')")
        print(f"# print(msg)")
        
        # Example 3: Extend license
        print("\n" + "-" * 80)
        print("مثال 3: تمديد ترخيص - Example 3: Extend License")
        print("-" * 80)
        print(f"الكود - Code:")
        print(f'  lc.extend_license("{demo_license}", days=60)')
        print(f"\nلتنفيذ هذا المثال، قم بإلغاء التعليق عن السطر التالي:")
        print(f"# success, msg = lc.extend_license('{demo_license}', days=60)")
        print(f"# print(msg)")
        
        # Example 4: Deactivate license
        print("\n" + "-" * 80)
        print("مثال 4: إلغاء تفعيل ترخيص - Example 4: Deactivate License")
        print("-" * 80)
        print(f"الكود - Code:")
        print(f'  lc.deactivate_license("{demo_license}")')
        print(f"\nلتنفيذ هذا المثال، قم بإلغاء التعليق عن السطر التالي:")
        print(f"# success, msg = lc.deactivate_license('{demo_license}')")
        print(f"# print(msg)")
    
    # Instructions
    print("\n" + "=" * 80)
    print("📝 كيفية الاستخدام - How to Use")
    print("=" * 80)
    print("""
1️⃣ لتنفيذ أي عملية:
   - قم بإلغاء التعليق عن السطر المطلوب
   - شغّل السكريبت مرة أخرى
   
2️⃣ لمشاهدة التغييرات في Control Panel:
   - افتح DED Control Panel
   - انتظر 30 ثانية للمزامنة التلقائية
   - أو اضغط زر "🔄 مزامنة" للمزامنة الفورية
   
3️⃣ لإنشاء سكريبت مخصص:
   - انسخ هذا الملف
   - عدّل العمليات حسب احتياجك
   - شغّل السكريبت

4️⃣ للاستخدام في تطبيق آخر:
   ```python
   from license_control import LicenseControl
   lc = LicenseControl()
   
   # استخدم الوظائف المتاحة
   licenses = lc.get_all_licenses()
   success, msg = lc.suspend_license("KEY", "reason")
   ```
    """)
    
    print("=" * 80)
    print("✅ انتهى - Done!")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ خطأ - Error: {e}")
        import traceback
        traceback.print_exc()

