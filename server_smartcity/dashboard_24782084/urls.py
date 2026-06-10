from django.urls import path

from .views import DashboardDataView, DashboardView


app_name = 'dashboard_24782084'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('data/', DashboardDataView.as_view(), name='data'),
]
