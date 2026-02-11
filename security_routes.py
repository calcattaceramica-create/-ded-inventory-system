from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app import db
from app.security import bp
from app.models import SecurityLog, IPWhitelist, SessionLog, User
from app.models_license import License, LicenseCheck
from app.license_manager import LicenseManager
from app.tenant_manager import TenantManager
from app.auth.decorators import admin_required, permission_required
from datetime import datetime, timedelta
from sqlalchemy import func, desc

@bp.route('/dashboard')
@login_required
@permission_required('security.view')
def dashboard():
    """Security dashboard"""
    # Get statistics
    total_logs = SecurityLog.query.count()
    failed_logins_today = SecurityLog.query.filter(
        SecurityLog.event_type == 'failed_login_wrong_password',
        SecurityLog.created_at >= datetime.utcnow().date()
    ).count()
    
    active_sessions = SessionLog.query.filter_by(is_active=True).count()
    locked_accounts = User.query.filter(
        User.account_locked_until != None,
        User.account_locked_until > datetime.utcnow()
    ).count()
    
    # Recent security events
    recent_events = SecurityLog.query.order_by(desc(SecurityLog.created_at)).limit(20).all()
    
    # Failed login attempts by IP
    failed_by_ip = db.session.query(
        SecurityLog.ip_address,
        func.count(SecurityLog.id).label('count')
    ).filter(
        SecurityLog.event_type.in_(['failed_login_wrong_password', 'failed_login_unknown_user']),
        SecurityLog.created_at >= datetime.utcnow() - timedelta(days=7)
    ).group_by(SecurityLog.ip_address).order_by(desc('count')).limit(10).all()
    
    # Active sessions
    active_sessions_list = SessionLog.query.filter_by(is_active=True).order_by(
        desc(SessionLog.last_activity)
    ).limit(10).all()
    
    return render_template('security/dashboard.html',
                         total_logs=total_logs,
                         failed_logins_today=failed_logins_today,
                         active_sessions=active_sessions,
                         locked_accounts=locked_accounts,
                         recent_events=recent_events,
                         failed_by_ip=failed_by_ip,
                         active_sessions_list=active_sessions_list)

@bp.route('/logs')
@login_required
@permission_required('security.view')
def logs():
    """View security logs"""
    page = request.args.get('page', 1, type=int)
    event_type = request.args.get('event_type', '')
    severity = request.args.get('severity', '')
    
    query = SecurityLog.query
    
    if event_type:
        query = query.filter_by(event_type=event_type)
    if severity:
        query = query.filter_by(severity=severity)
    
    logs = query.order_by(desc(SecurityLog.created_at)).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('security/logs.html', logs=logs)

@bp.route('/ip-whitelist')
@login_required
@permission_required('security.manage')
def ip_whitelist():
    """Manage IP whitelist"""
    ips = IPWhitelist.query.order_by(desc(IPWhitelist.created_at)).all()
    return render_template('security/ip_whitelist.html', ips=ips)

@bp.route('/ip-whitelist/add', methods=['POST'])
@login_required
@permission_required('security.manage')
def add_ip_whitelist():
    """Add IP to whitelist"""
    ip_address = request.form.get('ip_address')
    description = request.form.get('description')
    
    if not ip_address:
        flash('يرجى إدخال عنوان IP', 'danger')
        return redirect(url_for('security.ip_whitelist'))
    
    # Check if IP already exists
    existing = IPWhitelist.query.filter_by(ip_address=ip_address).first()
    if existing:
        flash('عنوان IP موجود بالفعل', 'warning')
        return redirect(url_for('security.ip_whitelist'))
    
    # Add to whitelist
    whitelist = IPWhitelist(
        ip_address=ip_address,
        description=description,
        created_by=current_user.id
    )
    db.session.add(whitelist)
    db.session.commit()
    
    flash('تم إضافة عنوان IP إلى القائمة البيضاء', 'success')
    return redirect(url_for('security.ip_whitelist'))

@bp.route('/ip-whitelist/delete/<int:id>')
@login_required
@permission_required('security.manage')
def delete_ip_whitelist(id):
    """Delete IP from whitelist"""
    whitelist = IPWhitelist.query.get_or_404(id)
    db.session.delete(whitelist)
    db.session.commit()
    
    flash('تم حذف عنوان IP من القائمة البيضاء', 'success')
    return redirect(url_for('security.ip_whitelist'))

@bp.route('/sessions')
@login_required
@permission_required('security.manage')
def sessions():
    """View active sessions"""
    active = SessionLog.query.filter_by(is_active=True).order_by(
        desc(SessionLog.last_activity)
    ).all()
    
    return render_template('security/sessions.html', sessions=active)

@bp.route('/sessions/terminate/<int:id>')
@login_required
@permission_required('security.manage')
def terminate_session(id):
    """Terminate a session"""
    session_log = SessionLog.query.get_or_404(id)
    session_log.is_active = False
    session_log.logout_at = datetime.utcnow()
    db.session.commit()
    
    flash('تم إنهاء الجلسة', 'success')
    return redirect(url_for('security.sessions'))

@bp.route('/users/unlock/<int:id>')
@login_required
@permission_required('security.manage')
def unlock_user(id):
    """Unlock a user account"""
    user = User.query.get_or_404(id)
    user.unlock_account()
    
    flash(f'تم فتح حساب {user.username}', 'success')
    return redirect(url_for('security.dashboard'))

@bp.route('/license')
@login_required
@permission_required('license.view')
def license_info():
    """License information and management"""
    licenses = LicenseManager.get_all_licenses()
    active_license = next((l for l in licenses if l.is_active), None)

    # Get stats for active license (simplified - no user count)
    stats = None
    if active_license:
        stats = {
            'current_users': 0,
            'max_users': active_license.max_users,
            'user_percentage': 0,
            'days_remaining': active_license.days_remaining()
        }

    return render_template('security/license.html',
                         licenses=licenses,
                         active_license=active_license,
                         stats=stats)

# DISABLED: License management moved to external control panel (DED_Control_Panel.pyw)
# Use DED_Control_Panel.pyw for all license management operations
@bp.route('/license/activate', methods=['POST'])
@login_required
@permission_required('license.manage')
def activate_license():
    """DISABLED: License management moved to external control panel"""
    flash('⚠️ إدارة التراخيص متاحة فقط من خلال لوحة التحكم الخارجية (DED Control Panel)', 'warning')
    flash('⚠️ License management is only available through the external control panel (DED Control Panel)', 'warning')
    return redirect(url_for('security.license_info'))

@bp.route('/license/users/<int:license_id>')
@login_required
@permission_required('license.view')
def license_users(license_id):
    """View users assigned to a license"""
    license = License.query.get_or_404(license_id)
    users = User.query.filter_by(license_id=license_id).all()
    all_users = User.query.filter(User.is_admin == False).all()

    return render_template('security/license_users.html',
                         license=license,
                         users=users,
                         all_users=all_users)

@bp.route('/license/details/<int:license_id>')
@login_required
@permission_required('license.view')
def license_details(license_id):
    """View detailed license information and statistics"""
    license = License.query.get_or_404(license_id)

    # Get users for this license
    users = User.query.filter_by(license_id=license_id).all()

    # Get statistics
    stats = {
        'total_users': len(users),
        'active_users': len([u for u in users if u.is_active]),
        'max_users': license.max_users,
        'days_remaining': license.days_remaining(),
        'is_expired': license.is_expired() if hasattr(license, 'is_expired') else False,
        'is_expiring_soon': license.days_remaining() <= 7 if license.days_remaining() else False,
    }

    return render_template('security/license_details.html',
                         license=license,
                         users=users,
                         stats=stats)

# DISABLED: Use DED_Control_Panel.pyw for license suspension
@bp.route('/license/suspend/<int:license_id>', methods=['POST'])
@login_required
@permission_required('license.manage')
def suspend_license(license_id):
    """DISABLED: License management moved to external control panel"""
    flash('⚠️ إدارة التراخيص متاحة فقط من خلال لوحة التحكم الخارجية (DED Control Panel)', 'warning')
    flash('⚠️ License management is only available through the external control panel (DED Control Panel)', 'warning')
    return redirect(url_for('security.license_info'))

# DISABLED: Use DED_Control_Panel.pyw for license reactivation
@bp.route('/license/reactivate/<int:license_id>', methods=['POST'])
@login_required
@permission_required('license.manage')
def reactivate_license(license_id):
    """DISABLED: License management moved to external control panel"""
    flash('⚠️ إدارة التراخيص متاحة فقط من خلال لوحة التحكم الخارجية (DED Control Panel)', 'warning')
    flash('⚠️ License management is only available through the external control panel (DED Control Panel)', 'warning')
    return redirect(url_for('security.license_info'))

# DISABLED: Use DED_Control_Panel.pyw for license deletion
@bp.route('/license/delete/<int:license_id>', methods=['POST'])
@login_required
@permission_required('license.manage')
def delete_license(license_id):
    """DISABLED: License management moved to external control panel"""
    flash('⚠️ إدارة التراخيص متاحة فقط من خلال لوحة التحكم الخارجية (DED Control Panel)', 'warning')
    flash('⚠️ License management is only available through the external control panel (DED Control Panel)', 'warning')
    return redirect(url_for('security.license_info'))

# DISABLED: Use DED_Control_Panel.pyw for user-license assignment
@bp.route('/license/assign-user', methods=['POST'])
@login_required
@permission_required('license.manage')
def assign_user_license():
    """DISABLED: License management moved to external control panel"""
    flash('⚠️ إدارة التراخيص متاحة فقط من خلال لوحة التحكم الخارجية (DED Control Panel)', 'warning')
    flash('⚠️ License management is only available through the external control panel (DED Control Panel)', 'warning')
    return redirect(url_for('security.license_info'))

# DISABLED: Use DED_Control_Panel.pyw for removing users from licenses
@bp.route('/license/remove-user/<int:user_id>')
@login_required
@permission_required('license.manage')
def remove_user_license(user_id):
    """DISABLED: License management moved to external control panel"""
    flash('⚠️ إدارة التراخيص متاحة فقط من خلال لوحة التحكم الخارجية (DED Control Panel)', 'warning')
    flash('⚠️ License management is only available through the external control panel (DED Control Panel)', 'warning')
    return redirect(url_for('security.license_info'))

# DISABLED: Use DED_Control_Panel.pyw for creating new licenses
@bp.route('/license/create', methods=['GET', 'POST'])
@login_required
@permission_required('license.manage')
def create_license():
    """DISABLED: License management moved to external control panel"""
    flash('⚠️ إدارة التراخيص متاحة فقط من خلال لوحة التحكم الخارجية (DED Control Panel)', 'warning')
    flash('⚠️ License management is only available through the external control panel (DED Control Panel)', 'warning')
    return redirect(url_for('security.license_info'))

