from django.db.models import Count
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from main_app.models import Report


class DashboardView(TemplateView):
    template_name = 'dashboard_24782084/index.html'


class DashboardDataView(View):
    def get(self, request, *args, **kwargs):
        status_counts = dict(
            Report.objects.values_list('status').annotate(total=Count('id'))
        )
        category_counts = dict(
            Report.objects.values_list('category').annotate(total=Count('id'))
        )

        reported_reports = Report.objects.filter(status='REPORTED')[:5]
        resolved_reports = Report.objects.filter(status='RESOLVED')[:5]

        return JsonResponse({
            'total': Report.objects.count(),
            'status': {
                key: status_counts.get(key, 0)
                for key, _ in Report.STATUS_CHOICES
            },
            'categories': {
                key: category_counts.get(key, 0)
                for key, _ in Report.CATEGORY_CHOICES
            },
            'latest_reported': [
                self.serialize_report(report) for report in reported_reports
            ],
            'latest_resolved': [
                self.serialize_report(report) for report in resolved_reports
            ],
        })

    def serialize_report(self, report):
        return {
            'id': report.id,
            'title': report.title,
            'category': report.category,
            'location': report.location,
            'status': report.status,
            'created_at': report.created_at.strftime('%d %b %Y %H:%M'),
        }
