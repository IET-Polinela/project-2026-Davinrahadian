#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('c:\\Users\\ASUS\\Documents\\project-2026-Davinrahadian')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from usermanagement_24782084.models import User

try:
    user = User.objects.get(username='admin')
    print(f'User found: {user.username}')
    print(f'is_admin: {user.is_admin}')
    print(f'is_active: {user.is_active}')
    print(f'Password check: {user.check_password("admin123")}')
except User.DoesNotExist:
    print('User admin not found, creating...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', is_admin=True)
    print('Admin user created successfully')