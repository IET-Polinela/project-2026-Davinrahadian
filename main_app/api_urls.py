from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from .api_views import RegisterView, ReportViewSet

router = DefaultRouter()
router.register('reports', ReportViewSet, basename='report')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
