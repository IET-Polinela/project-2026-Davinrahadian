
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST


def admin_required(view_func):
    @login_required
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if getattr(user, 'is_admin', False) or getattr(user, 'is_superuser', False):
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Akses ditolak: fitur ini khusus admin.')
        return redirect(request.META.get('HTTP_REFERER') or 'report_list')

    return _wrapped


@admin_required
@require_POST
def update_status(request, id):
    report = get_object_or_404(Report, id=id)

    # Workflow logic
    if report.status == 'REPORTED':
        report.status = 'VERIFIED'
    elif report.status == 'VERIFIED':
        report.status = 'IN_PROGRESS'
    elif report.status == 'IN_PROGRESS':
        report.status = 'RESOLVED'

    report.save()
    messages.success(request, 'Status berhasil diperbarui!')

    return redirect('report_list')
# =========================
# LIST REPORT
# =========================
@login_required
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'main_app/report_list.html', {'reports': reports})


@login_required
def report_search(request):
    query = request.GET.get('q', '').strip()
    reports = Report.objects.all()

    if query:
        reports = reports.filter(
            Q(title__icontains=query)
            | Q(category__icontains=query)
            | Q(location__icontains=query)
            | Q(description__icontains=query)
            | Q(status__icontains=query)
        )

    data = [
        {
            'id': report.id,
            'title': report.title,
            'category': report.category,
            'description': report.description,
            'location': report.location,
            'status': report.status,
        }
        for report in reports[:50]
    ]

    return JsonResponse({'reports': data})


@login_required
def report_json_detail(request, id):
    report = get_object_or_404(Report, id=id)
    return JsonResponse({
        'id': report.id,
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
        'created_at': report.created_at.strftime('%d %B %Y %H:%M'),
    })


# =========================
# ADD REPORT (manual form)
# =========================
@login_required
def add_report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Report.objects.create(
            title=title,
            reporter=request.user,
            category=request.POST.get('category') or 'Jalan Rusak',
            location=request.POST.get('location') or '-',
            description=description,
            status='REPORTED'  # ✅ FIX sesuai lab
        )

        messages.success(request, 'Laporan berhasil ditambahkan!')
        return redirect('report_list')

    return render(request, 'main_app/add_report.html')


# =========================
# CREATE REPORT (ModelForm)
# =========================
@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            messages.success(request, 'Laporan berhasil dibuat!')
            return redirect('report_list')
    else:
        form = ReportForm()

    return render(request, 'main_app/report_form.html', {'form': form})


# =========================
# DETAIL
# =========================
@login_required
def report_detail(request, id):
    report = get_object_or_404(Report, id=id)
    return render(request, 'main_app/report_detail.html', {'object': report})


# =========================
# UPDATE
# =========================
@admin_required
def update_report(request, id):
    report = get_object_or_404(Report, id=id)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laporan berhasil diupdate!')
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)

    return render(request, 'main_app/update_report.html', {'form': form})


# =========================
# DELETE
# =========================
@admin_required
def delete_report(request, id):
    report = get_object_or_404(Report, id=id)

    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Laporan berhasil dihapus!')
        return redirect('report_list')

    return render(request, 'main_app/report_confirm_delete.html', {'object': report})


# =========================
# HOME
# =========================
def home(request):
    total_reports = Report.objects.count()
    active_citizens = Report.objects.exclude(reporter__isnull=True).values('reporter').distinct().count()
    verified_reports = Report.objects.filter(status__in=['VERIFIED', 'IN_PROGRESS', 'RESOLVED']).count()
    resolved_reports = Report.objects.filter(status='RESOLVED').count()
    in_progress_reports = Report.objects.filter(status='IN_PROGRESS').count()
    recent_reports = Report.objects.select_related('reporter')[:5]

    ai_detection = round((verified_reports / total_reports) * 100) if total_reports else 96
    resolution_rate = round((resolved_reports / total_reports) * 100) if total_reports else 82
    response_time = 4 if total_reports else 3

    context = {
        'total_reports': total_reports,
        'active_citizens': active_citizens,
        'verified_reports': verified_reports,
        'resolved_reports': resolved_reports,
        'in_progress_reports': in_progress_reports,
        'ai_detection': ai_detection,
        'resolution_rate': resolution_rate,
        'response_time': response_time,
        'system_uptime': '99.98%',
        'recent_reports': recent_reports,
    }

    return render(request, 'main_app/home.html', context)


# =========================
# DASHBOARD (UPDATED STATUS)
# =========================
@admin_required
def dashboard(request):
    total = Report.objects.count()
    reported = Report.objects.filter(status='REPORTED').count()
    verified = Report.objects.filter(status='VERIFIED').count()
    in_progress = Report.objects.filter(status='IN_PROGRESS').count()
    resolved = Report.objects.filter(status='RESOLVED').count()
    category_counts = dict(
        Report.objects.values_list('category').annotate(total=Count('id'))
    )

    context = {
        'total': total,
        'reported': reported,
        'verified': verified,
        'in_progress': in_progress,
        'resolved': resolved,
        'jalan_rusak': category_counts.get('Jalan Rusak', 0),
        'sampah': category_counts.get('Sampah', 0),
        'lampu_mati': category_counts.get('Lampu Mati', 0),
        'drainase': category_counts.get('Drainase', 0),
        'keamanan': category_counts.get('Keamanan', 0),
    }

    return render(request, 'main_app/dashboard.html', context)
