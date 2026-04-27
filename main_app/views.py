
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
            form.save()
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
    return render(request, 'main_app/home.html')


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

    context = {
        'total': total,
        'reported': reported,
        'verified': verified,
        'in_progress': in_progress,
        'resolved': resolved,
    }

    return render(request, 'main_app/dashboard.html', context)
