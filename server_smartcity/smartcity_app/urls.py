from django.contrib import admin
from django.urls import path, include
from main_app.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main_app.api_urls')),
    path('', home, name='home'),
    path('dashboard/', include('dashboard_24782084.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('', include('main_app.urls')),
    path('', include('usermanagement_24782084.urls')),
]
