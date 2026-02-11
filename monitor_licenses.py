import sqlite3
from pathlib import Path
import time

db_path = Path('C:/Users/DELL/Desktop/DED_Portable_App/erp_system.db')

print("🔍 Monitoring licenses in database...")
print("="*80)
print("Waiting for new licenses to be added...")
print("Press Ctrl+C to stop")
print("="*80)

previous_count = 0

while True:
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM licenses')
        current_count = cursor.fetchone()[0]
        
        if current_count != previous_count:
            print(f"\n⚡ Change detected! Total licenses: {current_count}")
            print("-"*80)
            
            # Get latest license
            cursor.execute('''
                SELECT license_key, client_name, client_company, created_at
                FROM licenses
                ORDER BY created_at DESC
                LIMIT 1
            ''')
            
            latest = cursor.fetchone()
            if latest:
                print(f"📋 Latest License:")
                print(f"   Key: {latest[0]}")
                print(f"   Client: {latest[1]}")
                print(f"   Company: {latest[2]}")
                print(f"   Created: {latest[3]}")
                print("-"*80)
            
            previous_count = current_count
        
        conn.close()
        time.sleep(2)  # Check every 2 seconds
        
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped.")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(2)

