from usermanagement_24782084.models import User

# Fix admin permissions
admin = User.objects.get(username='admin')
admin.is_admin = True
admin.save()
print(f"Admin user updated: is_admin={admin.is_admin}")

# Ensure citizen has is_admin=False
citizen = User.objects.get(username='davin.07')
citizen.is_admin = False
citizen.save()
print(f"Citizen user updated: is_admin={citizen.is_admin}")

print("\n=== ALL USERS ===")
for user in User.objects.all():
    print(f"{user.username}: is_admin={user.is_admin}")
