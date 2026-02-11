"""
تحديث auth/routes.py لإزالة نظام التراخيص
Update auth/routes.py to remove license system
"""
import os

print("=" * 80)
print("🔧 تحديث auth/routes.py لإزالة نظام التراخيص")
print("🔧 Updating auth/routes.py to remove license system")
print("=" * 80)
print()

# المسار
routes_path = r"C:\Users\DELL\Desktop\DED_Portable_App\app\auth\routes.py"

# الكود الجديد بدون نظام التراخيص
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
    # قراءة الملف الحالي
    with open(routes_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("✅ تم قراءة الملف الحالي")
    
    # البحث عن بداية ونهاية دالة login
    start_marker = "@bp.route('/login', methods=['GET', 'POST'])"
    end_marker = "return render_template('auth/login.html')"
    
    start_index = content.find(start_marker)
    if start_index == -1:
        print("❌ لم يتم العثور على دالة login")
        exit(1)
    
    # البحث عن نهاية الدالة
    end_index = content.find(end_marker, start_index)
    if end_index == -1:
        print("❌ لم يتم العثور على نهاية دالة login")
        exit(1)
    
    # إضافة طول السطر الأخير
    end_index = content.find('\n', end_index) + 1
    
    # استبدال الدالة
    new_content = content[:start_index] + new_login_route + content[end_index:]
    
    # حفظ الملف
    with open(routes_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ تم تحديث ملف routes.py بنجاح")
    print()
    print("📝 التغييرات:")
    print("   - تمت إزالة license_key من نموذج تسجيل الدخول")
    print("   - تمت إزالة authenticate_with_license")
    print("   - تمت إزالة tenant_license_key من الجلسة")
    print("   - تم استخدام تسجيل دخول بسيط بدون تراخيص")
    
except Exception as e:
    print(f"❌ خطأ: {e}")

print()
print("=" * 80)
print("✅ تم!")
print("=" * 80)

