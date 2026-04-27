from usermanagement_24782084.models import User

# Cek user admin
try:
    user = User.objects.get(username='admin')
    print('User found:', user.username)
    print('is_admin:', user.is_admin)
    print('Password valid:', user.check_password('admin123'))
except User.DoesNotExist:
    print('Creating admin user...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', is_admin=True)
    print('Admin created')