from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
<<<<<<< HEAD
    path('contacts/', include('contacts.urls')),
=======
>>>>>>> 8426490 (Labsession4)
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
]