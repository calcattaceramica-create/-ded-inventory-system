from flask import render_template, redirect, url_for, flash, request, session, current_app, make_response
from flask_login import login_user, logout_user, current_user
from flask_babel import gettext as _
from app import db
from app.auth import bp
from app.models import User, SecurityLog, SessionLog
# License system removed - no longer needed
from datetime import datetime
import uuid

def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def log_security_event(user_id, event_type, details=None, severity='info'):
    """Log security event"""
    try:
        log = SecurityLog(
            user_id=user_id,
            event_type=event_type,
            ip_address=get_client_ip(),
            user_agent=request.headers.get('User-Agent', '')[:256],
            details=details,
            severity=severity
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging security event: {e}")

# License check function removed - no license system

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        # Simple authentication - no license required
        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            log_security_event(None, 'failed_login',
                             f'Failed login attempt for username: {username}', 'warning')
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
            return redirect(url_for('auth.login'))

        # Check if user is active
        if not user.is_active:
            log_security_event(user.id, 'failed_login',
                             f'Login attempt for inactive user: {username}', 'warning')
            flash('الحساب غير نشط. يرجى التواصل مع المسؤول', 'danger')
            return redirect(url_for('auth.login'))

        # Clear session completely (EXCEPT Flask-Login internal keys)
        keys_to_remove = [key for key in session.keys() if not key.startswith('_')]
        for key in keys_to_remove:
            session.pop(key, None)

        # Login the user
        login_user(user, remember=remember)
        print(f"✅ LOGIN: Logged in user: {user.username}")

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
        log_security_event(user.id, 'successful_login',
                         f'Successful login from {get_client_ip()}', 'info')

        # Set user language in session
        session['language'] = user.language

        # Check if password change is required
        if user.must_change_password:
            flash('يجب عليك تغيير كلمة المرور', 'warning')
            response = make_response(redirect(url_for('auth.change_password')))
            # Add cache-busting headers
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')

        flash(f'مرحباً {user.full_name}!', 'success')

        # Create response with cache-busting headers to prevent browser caching
        response = make_response(redirect(next_page))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        print(f"✅ LOGIN: Redirecting to {next_page} with cache-busting headers")
        return response

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        # Update session log
        session_id = session.get('session_id')
        if session_id:
            session_log = SessionLog.query.filter_by(session_id=session_id).first()
            if session_log:
                session_log.logout_at = datetime.utcnow()
                session_log.is_active = False
                db.session.commit()

        # Log logout event
        log_security_event(current_user.id, 'logout', 'User logged out', 'info')

        logout_user()

        # Clear all session data
        session.clear()
        print(f"🔥 LOGOUT: Cleared all session data")

        flash('تم تسجيل الخروج بنجاح', 'info')

    # Create response with cache-busting headers
    response = make_response(redirect(url_for('auth.login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    print(f"✅ LOGOUT: Redirecting to login with cache-busting headers")
    return response

@bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validate current password
        if not current_user.check_password(current_password):
            flash('كلمة المرور الحالية غير صحيحة', 'danger')
            return redirect(url_for('auth.change_password'))

        # Validate new password
        if len(new_password) < 8:
            flash('كلمة المرور يجب أن تكون 8 أحرف على الأقل', 'danger')
            return redirect(url_for('auth.change_password'))

        if new_password != confirm_password:
            flash('كلمة المرور الجديدة وتأكيد كلمة المرور غير متطابقتين', 'danger')
            return redirect(url_for('auth.change_password'))

        # Check password strength
        if not any(c.isupper() for c in new_password):
            flash('كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل', 'danger')
            return redirect(url_for('auth.change_password'))

        if not any(c.isdigit() for c in new_password):
            flash('كلمة المرور يجب أن تحتوي على رقم واحد على الأقل', 'danger')
            return redirect(url_for('auth.change_password'))

        # Update password
        current_user.set_password(new_password)
        current_user.password_changed_at = datetime.utcnow()
        current_user.must_change_password = False
        db.session.commit()

        # Log password change
        log_security_event(current_user.id, 'password_changed',
                         'User changed password', 'info')

        flash('تم تغيير كلمة المرور بنجاح', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/change_password.html')

@bp.route('/change-language/<lang>')
def change_language(lang):
    if lang in ['ar', 'en']:
        session['language'] = lang
        if current_user.is_authenticated:
            current_user.language = lang
            db.session.commit()
    return redirect(request.referrer or url_for('main.index'))

