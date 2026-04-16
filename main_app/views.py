
from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm
from django.contrib import messages

from django.views.decorators.http import require_POST

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
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'main_app/report_list.html', {'reports': reports})


# =========================
# ADD REPORT (manual form)
# =========================
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
def report_detail(request, id):
    report = get_object_or_404(Report, id=id)
    return render(request, 'main_app/report_detail.html', {'object': report})


# =========================
# UPDATE
# =========================
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