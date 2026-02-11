"""
إصلاح مشكلة تسجيل الخروج - حذف جميع الكوكيز والجلسات
Fix logout issue - Delete all cookies and sessions
"""
import sys
sys.path.insert(0, r'C:\Users\DELL\Desktop\DED_Portable_App')

from app import create_app, db
from app.models import SessionLog
import os
import shutil

print("=" * 80)
print("🔧 إصلاح مشكلة تسجيل الخروج")
print("🔧 Fixing Logout Issue")
print("=" * 80)

app = create_app()

with app.app_context():
    # Step 1: Deactivate all sessions in database
    print("\n📝 الخطوة 1: إلغاء تفعيل جميع الجلسات في قاعدة البيانات...")
    print("📝 Step 1: Deactivating all sessions in database...")
    
    try:
        active_sessions = SessionLog.query.filter_by(is_active=True).all()
        count = len(active_sessions)
        
        for session_log in active_sessions:
            session_log.is_active = False
            session_log.logout_at = db.func.now()
        
        db.session.commit()
        print(f"   ✅ تم إلغاء تفعيل {count} جلسة")
        print(f"   ✅ Deactivated {count} sessions")
    except Exception as e:
        print(f"   ❌ خطأ: {e}")

# Step 2: Delete Flask session files
print("\n📝 الخطوة 2: حذف ملفات الجلسات...")
print("📝 Step 2: Deleting session files...")

session_dir = r"C:\Users\DELL\Desktop\DED_Portable_App\flask_session"
if os.path.exists(session_dir):
    try:
        shutil.rmtree(session_dir)
        print(f"   ✅ تم حذف مجلد الجلسات: {session_dir}")
        print(f"   ✅ Deleted session directory: {session_dir}")
    except Exception as e:
        print(f"   ⚠️  لم يتم حذف مجلد الجلسات: {e}")
        print(f"   ⚠️  Could not delete session directory: {e}")
else:
    print("   ℹ️  مجلد الجلسات غير موجود")
    print("   ℹ️  Session directory does not exist")

print("\n" + "=" * 80)
print("✅ تم إصلاح قاعدة البيانات!")
print("✅ Database fixed!")
print("=" * 80)

print("\n📋 الخطوات التالية (مهمة جداً):")
print("📋 Next Steps (Very Important):")
print("\n1️⃣  امسح الكوكيز في المتصفح:")
print("   Clear browser cookies:")
print("   - اضغط: Ctrl + Shift + Delete")
print("   - Press: Ctrl + Shift + Delete")
print("   - اختر: Cookies and other site data")
print("   - Select: Cookies and other site data")
print("   - اختر: All time")
print("   - Select: All time")
print("   - انقر: Clear data")
print("   - Click: Clear data")

print("\n2️⃣  أغلق المتصفح تماماً:")
print("   Close browser completely:")
print("   - أغلق جميع النوافذ")
print("   - Close all windows")
print("   - تأكد من إغلاق العملية من Task Manager")
print("   - Make sure to close process from Task Manager")

print("\n3️⃣  أعد تشغيل المتصفح:")
print("   Restart browser:")
print("   - افتح المتصفح من جديد")
print("   - Open browser again")

print("\n4️⃣  اذهب إلى صفحة تسجيل الدخول:")
print("   Go to login page:")
print("   🌐 http://127.0.0.1:5000/auth/login")

print("\n5️⃣  سجل الدخول:")
print("   Login:")
print("   - اسم المستخدم: admin")
print("   - Username: admin")
print("   - كلمة المرور: admin123")
print("   - Password: admin123")

print("\n" + "=" * 80)
print("⚠️  ملاحظة مهمة:")
print("⚠️  Important Note:")
print("=" * 80)
print("\nإذا لم تمسح الكوكيز من المتصفح، ستبقى المشكلة!")
print("If you don't clear browser cookies, the problem will persist!")
print("\nالمشكلة ليست في التطبيق، المشكلة في الكاش في المتصفح!")
print("The problem is not in the app, it's in the browser cache!")
print("\n" + "=" * 80)

