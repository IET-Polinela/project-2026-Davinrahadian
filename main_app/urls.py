from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('create/', views.create_report, name='create_report'),
    path('detail/<int:id>/', views.report_detail, name='report_detail'),
    path('update/<int:id>/', views.update_report, name='update_report'),
  path('reports/', views.report_list, name='report_list'),
  path('delete/<int:id>/', views.delete_report, name='delete_report'),
  path('add/', views.add_report, name='add_report'),
]