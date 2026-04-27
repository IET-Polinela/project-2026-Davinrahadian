from usermanagement_24782084.models import User

print("\n=== USER PERMISSIONS ===")
for user in User.objects.all():
    print(f"Username: {user.username}")
    print(f"  is_admin: {user.is_admin}")
    print(f"  is_staff: {user.is_staff}")
    print(f"  is_superuser: {user.is_superuser}")
    print()
