#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix base.html template - Remove license_info reference
"""

import os

base_template_path = r'C:\Users\DELL\Desktop\DED_Portable_App\app\templates\base.html'

print("=" * 70)
print("🔧 Fixing base.html Template")
print("=" * 70)
print()

# Read the file
with open(base_template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and remove the license management section
lines = content.split('\n')
new_lines = []
skip_until_endif = False
skip_count = 0

for i, line in enumerate(lines):
    # Check if this is the license.view permission check
    if "current_user.has_permission('license.view')" in line:
        skip_until_endif = True
        skip_count = 0
        print(f"⚠️  Found license section at line {i+1}")
        continue
    
    # Skip lines until we find the matching endif
    if skip_until_endif:
        skip_count += 1
        if '{% endif %}' in line and skip_count <= 7:  # The endif for license section
            skip_until_endif = False
            print(f"✅ Removed license section ({skip_count} lines)")
            continue
    
    if not skip_until_endif:
        new_lines.append(line)

# Write back
new_content = '\n'.join(new_lines)
with open(base_template_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print()
print("=" * 70)
print("✅ base.html template fixed successfully!")
print("=" * 70)

