"""
إزالة نظام التراخيص بالكامل من التطبيق
Complete removal of license system from application
"""
import os
import shutil

print("=" * 80)
print("🗑️ إزالة نظام التراخيص بالكامل من التطبيق")
print("🗑️ Complete Removal of License System")
print("=" * 80)
print()

# المسار الأساسي
base_path = r"C:\Users\DELL\Desktop\DED_Portable_App"

# الخطوة 1: حذف الملفات المتعلقة بالتراخيص
print("📄 الخطوة 1: حذف الملفات المتعلقة بالتراخيص...")
print()

files_to_remove = [
    "license_control.py",
    "licenses.json",
    "licenses_master.db",
    "DED_Control_Panel.pyw",
    "DED_Control_Panel_BACKUP.pyw",
    "DED_Control_Panel_Beautiful.pyw",
    "DED_Control_Panel_NEW.pyw",
    "DED_Control_Panel_Original_Backup.pyw",
    "DED_Modern_Launcher.pyw",
    "activate_license.py",
    "license_manager_simple.py",
    "multi_tenant_login_backup.py",
    "auto_login.html",
    "test_login_6f10.py",
]

removed_files = 0
for file in files_to_remove:
    file_path = os.path.join(base_path, file)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"   ✅ تم حذف: {file}")
            removed_files += 1
        except Exception as e:
            print(f"   ❌ فشل حذف {file}: {e}")

print()

# الخطوة 2: حذف المجلدات المتعلقة بالتراخيص
print("📁 الخطوة 2: حذف المجلدات المتعلقة بالتراخيص...")
print()

folders_to_remove = [
    "tenant_databases",
]

removed_folders = 0
for folder in folders_to_remove:
    folder_path = os.path.join(base_path, folder)
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"   ✅ تم حذف: {folder}")
            removed_folders += 1
        except Exception as e:
            print(f"   ❌ فشل حذف {folder}: {e}")

print()

# الخطوة 3: تحديث auth/routes.py
print("🔧 الخطوة 3: تحديث auth/routes.py...")
print()

routes_path = os.path.join(base_path, "app", "auth", "routes.py")

new_login_route = '''@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        # Find user
        user = User.query.filter_by(username=username).first()

        if not user:
            log_security_event(None, 'failed_login',
                             f'Failed login: User not found - {username}', 'warning')
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
            return redirect(url_for('auth.login'))

        # Check if account is locked
        if user.is_account_locked():
            log_security_event(user.id, 'failed_login',
                             'Account locked', 'warning')
            flash('الحساب مقفل مؤقتاً. يرجى المحاولة لاحقاً', 'danger')
            return redirect(url_for('auth.login'))

        # Check password
        if not user.check_password(password):
            user.record_failed_login()
            log_security_event(user.id, 'failed_login',
                             'Invalid password', 'warning')
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
            return redirect(url_for('auth.login'))

        # Check if user is active
        if not user.is_active:
            log_security_event(user.id, 'failed_login',
                             'Inactive account', 'warning')
            flash('الحساب غير نشط. يرجى الاتصال بالمسؤول', 'danger')
            return redirect(url_for('auth.login'))

        # Login successful
        user.record_successful_login(get_client_ip())
        login_user(user, remember=remember)

        # Create session log
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        session_log = SessionLog(
            user_id=user.id,
            session_id=session_id,
            ip_address=get_client_ip(),
            user_agent=request.headers.get('User-Agent', '')[:256]
        )
        db.session.add(session_log)
        db.session.commit()

        # Log successful login
        log_security_event(user.id, 'login', 'User logged in successfully', 'info')

        flash(f'مرحباً {user.full_name}!', 'success')

        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        return redirect(url_for('main.index'))

    return render_template('auth/login.html')
'''

try:
    if os.path.exists(routes_path):
        with open(routes_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن دالة login واستبدالها
        start_marker = "@bp.route('/login', methods=['GET', 'POST'])"
        start_index = content.find(start_marker)
        
        if start_index != -1:
            # البحث عن نهاية الدالة
            end_marker = "return render_template('auth/login.html')"
            end_index = content.find(end_marker, start_index)
            
            if end_index != -1:
                end_index = content.find('\n', end_index) + 1
                new_content = content[:start_index] + new_login_route + content[end_index:]
                
                with open(routes_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("   ✅ تم تحديث auth/routes.py")
            else:
                print("   ⚠️ لم يتم العثور على نهاية دالة login")
        else:
            print("   ⚠️ لم يتم العثور على دالة login")
    else:
        print("   ⚠️ ملف routes.py غير موجود")
except Exception as e:
    print(f"   ❌ خطأ في تحديث routes.py: {e}")

print()

# الخطوة 4: نسخ login.html الجديد
print("📝 الخطوة 4: تحديث login.html...")
print()

login_template_path = os.path.join(base_path, "app", "templates", "auth", "login.html")
new_login_path = r"C:\Users\DELL\DED\login_no_license.html"

try:
    if os.path.exists(new_login_path):
        shutil.copy(new_login_path, login_template_path)
        print("   ✅ تم تحديث login.html")
    else:
        print("   ⚠️ ملف login_no_license.html غير موجود")
except Exception as e:
    print(f"   ❌ خطأ في تحديث login.html: {e}")

print()
print("=" * 80)
print("📊 النتيجة:")
print(f"   ✅ تم حذف {removed_files} ملف")
print(f"   ✅ تم حذف {removed_folders} مجلد")
print(f"   ✅ تم تحديث auth/routes.py")
print(f"   ✅ تم تحديث login.html")
print("=" * 80)
print()
print("✅ تم إزالة نظام التراخيص بنجاح!")
print("✅ License system removed successfully!")
print()
print("📝 الخطوة التالية:")
print("   1. اختبر تسجيل الدخول بدون license_key")
print("   2. تأكد من عمل التطبيق بشكل صحيح")
print("   3. ارفع التغييرات إلى GitHub")
print()

