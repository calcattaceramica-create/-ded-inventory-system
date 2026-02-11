"""
Prepare Render Deployment - Remove License System for Render Only
This script will:
1. Clone the repository
2. Create a new branch 'render-no-license'
3. Remove license system files
4. Update auth/routes.py and login.html
5. Push to GitHub
"""

import os
import shutil
import subprocess

print("=" * 80)
print("🚀 تحضير النشر على Render - إزالة نظام التراخيص")
print("🚀 Preparing Render Deployment - Removing License System")
print("=" * 80)
print()

# Configuration
REPO_URL = "https://github.com/calcattaceramica-create/ded-inventory-system.git"
CLONE_DIR = r"C:\Users\DELL\DED\ded-render-deployment"
BRANCH_NAME = "render-no-license"

# Step 1: Clone the repository
print("📥 الخطوة 1: استنساخ المستودع...")
print("📥 Step 1: Cloning repository...")
print()

if os.path.exists(CLONE_DIR):
    print(f"⚠️  المجلد موجود بالفعل: {CLONE_DIR}")
    print(f"⚠️  Directory already exists: {CLONE_DIR}")
    response = input("هل تريد حذفه والمتابعة؟ (y/n): ")
    if response.lower() == 'y':
        shutil.rmtree(CLONE_DIR)
        print("✅ تم حذف المجلد القديم")
    else:
        print("❌ تم الإلغاء")
        exit(0)

try:
    subprocess.run(["git", "clone", REPO_URL, CLONE_DIR], check=True)
    print("✅ تم استنساخ المستودع بنجاح")
    print()
except Exception as e:
    print(f"❌ خطأ في الاستنساخ: {e}")
    exit(1)

# Step 2: Create new branch
print("🌿 الخطوة 2: إنشاء branch جديد...")
print("🌿 Step 2: Creating new branch...")
print()

os.chdir(CLONE_DIR)

try:
    subprocess.run(["git", "checkout", "-b", BRANCH_NAME], check=True)
    print(f"✅ تم إنشاء branch: {BRANCH_NAME}")
    print()
except Exception as e:
    print(f"❌ خطأ في إنشاء branch: {e}")
    exit(1)

# Step 3: Remove license files
print("🗑️  الخطوة 3: حذف ملفات التراخيص...")
print("🗑️  Step 3: Removing license files...")
print()

files_to_remove = [
    "license_control.py",
    "licenses.json",
    "DED_Control_Panel.pyw"
]

removed_count = 0
for file in files_to_remove:
    file_path = os.path.join(CLONE_DIR, file)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"   ✅ تم حذف: {file}")
        removed_count += 1
    else:
        print(f"   ⚠️  غير موجود: {file}")

print()
print(f"✅ تم حذف {removed_count} ملف")
print()

# Step 4: Update auth/routes.py
print("📝 الخطوة 4: تحديث auth/routes.py...")
print("📝 Step 4: Updating auth/routes.py...")
print()

auth_routes_path = os.path.join(CLONE_DIR, "app", "auth", "routes.py")

# Read the local version (without license)
local_auth_routes = r"C:\Users\DELL\Desktop\DED_Portable_App\app\auth\routes.py"

try:
    with open(local_auth_routes, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(auth_routes_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ تم تحديث auth/routes.py")
    print()
except Exception as e:
    print(f"   ❌ خطأ: {e}")

# Step 5: Update login.html
print("📝 الخطوة 5: تحديث login.html...")
print("📝 Step 5: Updating login.html...")
print()

login_html_path = os.path.join(CLONE_DIR, "app", "templates", "auth", "login.html")
local_login_html = r"C:\Users\DELL\Desktop\DED_Portable_App\app\templates\auth\login.html"

try:
    with open(local_login_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(login_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ تم تحديث login.html")
    print()
except Exception as e:
    print(f"   ❌ خطأ: {e}")

# Step 6: Commit changes
print("💾 الخطوة 6: حفظ التغييرات...")
print("💾 Step 6: Committing changes...")
print()

try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Remove license system for Render deployment"], check=True)
    print("✅ تم حفظ التغييرات")
    print()
except Exception as e:
    print(f"❌ خطأ في الحفظ: {e}")
    exit(1)

print("=" * 80)
print("✅ تم تحضير النشر بنجاح!")
print("✅ Deployment prepared successfully!")
print("=" * 80)
print()
print("🎯 الخطوة التالية:")
print("🎯 Next step:")
print()
print(f"   cd {CLONE_DIR}")
print(f"   git push origin {BRANCH_NAME}")
print()
print("ثم على Render، اختر branch: render-no-license")
print("Then on Render, select branch: render-no-license")
print()

