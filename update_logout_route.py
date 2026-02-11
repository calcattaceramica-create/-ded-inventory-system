"""
تحديث كود تسجيل الخروج لحذف الكوكيز بشكل صريح
Update logout route to explicitly delete cookies
"""
import os

# Read the file
file_path = r'C:\Users\DELL\Desktop\DED_Portable_App\app\auth\routes.py'

print("=" * 80)
print("🔧 تحديث كود تسجيل الخروج")
print("🔧 Updating Logout Route")
print("=" * 80)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Old logout code
old_code = """    # Create response with cache-busting headers
    response = make_response(redirect(url_for('auth.login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    print(f"✅ LOGOUT: Redirecting to login with cache-busting headers")
    return response"""

# New logout code with explicit cookie deletion
new_code = """    # Create response with cache-busting headers
    response = make_response(redirect(url_for('auth.login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # CRITICAL: Explicitly delete session cookies
    # This forces the browser to remove the cookies
    response.set_cookie('session', '', expires=0, max_age=0, path='/')
    response.set_cookie('remember_token', '', expires=0, max_age=0, path='/')
    
    print(f"✅ LOGOUT: Redirecting to login with cache-busting headers and deleted cookies")
    return response"""

# Replace the code
if old_code in content:
    content = content.replace(old_code, new_code)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ تم تحديث كود تسجيل الخروج بنجاح!")
    print("✅ Logout route updated successfully!")
    print("\n📝 التغييرات:")
    print("   - تم إضافة حذف صريح للكوكيز")
    print("   - Added explicit cookie deletion")
    print("   - response.set_cookie('session', '', expires=0)")
    print("   - response.set_cookie('remember_token', '', expires=0)")
else:
    print("\n⚠️  لم يتم العثور على الكود القديم!")
    print("⚠️  Old code not found!")
    print("\n🔍 البحث عن كود تسجيل الخروج...")
    
    # Find logout route
    if '@bp.route(\'/logout\')' in content:
        print("✅ تم العثور على route تسجيل الخروج")
        
        # Show the current logout code
        start_idx = content.find('@bp.route(\'/logout\')')
        end_idx = content.find('@bp.route', start_idx + 1)
        if end_idx == -1:
            end_idx = len(content)
        
        logout_code = content[start_idx:end_idx]
        print("\n📄 الكود الحالي:")
        print(logout_code[:500])
    else:
        print("❌ لم يتم العثور على route تسجيل الخروج!")

print("\n" + "=" * 80)
print("📋 الخطوات التالية:")
print("=" * 80)
print("\n1️⃣  أعد تشغيل التطبيق:")
print("   - أغلق التطبيق الحالي (Ctrl + C)")
print("   - شغّل التطبيق من جديد")
print("\n2️⃣  امسح الكوكيز في المتصفح:")
print("   - اضغط: Ctrl + Shift + Delete")
print("   - اختر: Cookies and other site data")
print("   - اختر: All time")
print("   - انقر: Clear data")
print("\n3️⃣  أغلق المتصفح تماماً وأعد فتحه")
print("\n4️⃣  اذهب إلى: http://127.0.0.1:5000/auth/login")
print("\n5️⃣  سجل الدخول وجرب تسجيل الخروج")
print("\n" + "=" * 80)

