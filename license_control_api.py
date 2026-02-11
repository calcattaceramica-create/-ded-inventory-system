"""
License Control API Server
خادم API للتحكم في التراخيص من الخارج
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Database path
DB_PATH = Path('C:/Users/DELL/Desktop/DED_Portable_App/licenses_master.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/licenses', methods=['GET'])
def get_licenses():
    """Get all licenses"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT license_key, client_name, client_company, admin_username,
                   is_active, is_suspended, expires_at, created_at, max_users
            FROM licenses
            ORDER BY created_at DESC
        ''')
        
        licenses = []
        for row in cursor.fetchall():
            licenses.append({
                'license_key': row['license_key'],
                'client_name': row['client_name'],
                'client_company': row['client_company'],
                'admin_username': row['admin_username'],
                'is_active': bool(row['is_active']),
                'is_suspended': bool(row['is_suspended']),
                'expires_at': row['expires_at'],
                'created_at': row['created_at'],
                'max_users': row['max_users']
            })
        
        conn.close()
        return jsonify({'success': True, 'licenses': licenses})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/license/<license_key>/activate', methods=['POST'])
def activate_license(license_key):
    """Activate a license"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE licenses
            SET is_active = 1, is_suspended = 0, suspension_reason = NULL
            WHERE license_key = ?
        ''', (license_key,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'تم تفعيل الترخيص بنجاح'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/license/<license_key>/suspend', methods=['POST'])
def suspend_license(license_key):
    """Suspend a license"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'تم الإيقاف من لوحة التحكم')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE licenses
            SET is_suspended = 1, suspension_reason = ?
            WHERE license_key = ?
        ''', (reason, license_key))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'تم إيقاف الترخيص بنجاح'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/license/<license_key>/deactivate', methods=['POST'])
def deactivate_license(license_key):
    """Deactivate a license"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE licenses
            SET is_active = 0
            WHERE license_key = ?
        ''', (license_key,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'تم إلغاء تفعيل الترخيص بنجاح'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/license/<license_key>/extend', methods=['POST'])
def extend_license(license_key):
    """Extend license expiration"""
    try:
        data = request.get_json() or {}
        days = data.get('days', 30)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get current expiration
        cursor.execute('SELECT expires_at FROM licenses WHERE license_key = ?', (license_key,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({'success': False, 'error': 'الترخيص غير موجود'}), 404
        
        current_expires = row['expires_at']
        
        # Parse current expiration
        if current_expires:
            try:
                expires_dt = datetime.strptime(current_expires, '%Y-%m-%d %H:%M:%S')
            except:
                expires_dt = datetime.now()
        else:
            expires_dt = datetime.now()
        
        # Add days
        new_expires = expires_dt + timedelta(days=days)
        
        cursor.execute('''
            UPDATE licenses
            SET expires_at = ?
            WHERE license_key = ?
        ''', (new_expires.strftime('%Y-%m-%d %H:%M:%S'), license_key))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'تم تمديد الترخيص لمدة {days} يوم',
            'new_expires': new_expires.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("="*80)
    print("🚀 License Control API Server")
    print("="*80)
    print(f"Database: {DB_PATH}")
    print(f"Server: http://127.0.0.1:5001")
    print("="*80)
    print()
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)

