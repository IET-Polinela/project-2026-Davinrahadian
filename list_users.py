from usermanagement_24782084.models import User

print("\n=== ALL USERS ===")
for user in User.objects.all():
    print(f"Username: {user.username}, is_admin: {user.is_admin}")

# Set admin is_admin=True
admin = User.objects.get(username='admin')
admin.is_admin = True
admin.save()
print(f"\nAdmin user fixed: is_admin={admin.is_admin}")

# List all users again
print("\n=== AFTER FIX ===")
for user in User.objects.all():
    print(f"Username: {user.username}, is_admin: {user.is_admin}")
