"""
Create Admin User in Main Database
إنشاء مستخدم مدير في قاعدة البيانات الرئيسية
"""

import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin_user():
    """Create admin user in erp_system.db"""
    
    db_path = "C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db"
    
    print("=" * 70)
    print("🔧 Creating Admin User")
    print("=" * 70)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if admin user exists
        cursor.execute("SELECT id, username FROM users WHERE username = 'admin'")
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"✅ Admin user already exists (ID: {existing_user[0]})")
            
            # Update password
            password_hash = generate_password_hash('admin123')
            cursor.execute("""
                UPDATE users 
                SET password_hash = ?, is_active = 1, is_admin = 1
                WHERE username = 'admin'
            """, (password_hash,))
            conn.commit()
            print("✅ Updated admin password to: admin123")
            
        else:
            # Create new admin user
            password_hash = generate_password_hash('admin123')
            
            cursor.execute("""
                INSERT INTO users 
                (username, email, password_hash, full_name, is_active, is_admin, language, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'admin',
                'admin@ded-erp.com',
                password_hash,
                'مدير النظام',
                1,  # is_active
                1,  # is_admin
                'ar',  # language
                datetime.now()
            ))
            conn.commit()
            print("✅ Created new admin user")
        
        # Display all users
        cursor.execute("SELECT id, username, email, is_active, is_admin FROM users")
        users = cursor.fetchall()
        
        print("\n📊 Users in database:")
        print("-" * 70)
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Active: {user[3]}, Admin: {user[4]}")
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ Admin user ready!")
        print("=" * 70)
        print("\n📝 Login credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🌐 Login URL: http://127.0.0.1:5000/auth/login")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_admin_user()

