from rest_framework import generics, permissions, viewsets

from .models import Report
from .permissions import IsReportOwnerAndDraft
from .serializers import RegisterSerializer, ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

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
