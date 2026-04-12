from django.urls import path
from .views import (
    ReportListView,
    ReportDetailView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView
)

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name='home'),
    path('add/', views.add_report, name='add_report'),
    path('update/<int:id>/', views.update_report, name='update_report'),
    path('delete/<int:id>/', views.delete_report, name='delete_report'),
=======
    # LIST
    path('', ReportListView.as_view(), name='report_list'),

    # DETAIL
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),

    # CREATE
    path('create/', ReportCreateView.as_view(), name='report_create'),

    # UPDATE
    path('update/<int:pk>/', ReportUpdateView.as_view(), name='report_update'),

    # DELETE
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),

    # WORKFLOW STATUS
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='report_update_status'),
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),
>>>>>>> 8426490 (Labsession4)
]