"""
حذف جميع الجلسات القديمة
Clear all old sessions
"""
import sqlite3
import os

print("=" * 80)
print("🔧 حذف جميع الجلسات القديمة")
print("🔧 Clearing all old sessions")
print("=" * 80)

# Database path
db_path = r"C:\Users\DELL\Desktop\DED_Portable_App\erp_system.db"

if not os.path.exists(db_path):
    print(f"\n❌ قاعدة البيانات غير موجودة: {db_path}")
    exit(1)

print(f"\n📂 قاعدة البيانات: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if session_logs table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='session_logs'")
    if cursor.fetchone():
        # Count active sessions
        cursor.execute("SELECT COUNT(*) FROM session_logs WHERE is_active = 1")
        active_count = cursor.fetchone()[0]
        print(f"\n📊 عدد الجلسات النشطة: {active_count}")
        
        # Deactivate all sessions
        cursor.execute("UPDATE session_logs SET is_active = 0")
        conn.commit()
        print("✅ تم إلغاء تفعيل جميع الجلسات")
    else:
        print("\n⚠️  جدول session_logs غير موجود")
    
    # Also clear Flask sessions directory if it exists
    session_dir = r"C:\Users\DELL\Desktop\DED_Portable_App\flask_session"
    if os.path.exists(session_dir):
        import shutil
        try:
            shutil.rmtree(session_dir)
            print(f"✅ تم حذف مجلد الجلسات: {session_dir}")
        except Exception as e:
            print(f"⚠️  لم يتم حذف مجلد الجلسات: {e}")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ تم حذف جميع الجلسات بنجاح!")
    print("✅ All sessions cleared successfully!")
    print("=" * 80)
    
    print("\n📋 الخطوات التالية:")
    print("1. امسح الكوكيز في المتصفح:")
    print("   - اضغط Ctrl + Shift + Delete")
    print("   - اختر 'Cookies and other site data'")
    print("   - انقر 'Clear data'")
    print("\n2. اذهب إلى صفحة تسجيل الدخول:")
    print("   🌐 http://127.0.0.1:5000/auth/login")
    print("\n3. سجل الدخول:")
    print("   - اسم المستخدم: admin")
    print("   - كلمة المرور: admin123")
    
except Exception as e:
    print(f"\n❌ خطأ: {str(e)}")
    import traceback
    traceback.print_exc()

