from rest_framework import generics, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Report
from .permissions import IsReportOwnerAndDraft
from .serializers import RegisterSerializer, ReportSerializer


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_queryset(self):
        queryset = Report.objects.all().order_by('-updated_at')
        tab = self.request.query_params.get('tab')

        if tab == 'my_reports':
            return queryset.filter(reporter=self.request.user)

        if tab == 'feed':
            return queryset.exclude(status='DRAFT')

        return queryset

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsReportOwnerAndDraft]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
