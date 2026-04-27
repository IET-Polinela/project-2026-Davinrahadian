from django.urls import path, include
from main_app.views import home

urlpatterns = [
    path('', home, name='home'),
    path('', include('main_app.urls')),
    path('', include('usermanagement_24782084.urls')),
]