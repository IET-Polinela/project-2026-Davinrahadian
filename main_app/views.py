
from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm
from .models import Report

# LIST REPORT
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'main_app/report_list.html', {'reports': reports})

# ADD REPORT
def add_report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Report.objects.create(
            title=title,
            description=description,
            status='Pending'
        )
        return redirect('report_list')

    return render(request, 'main_app/add_report.html')
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'main_app/report_form.html', {'form': form})


def report_detail(request, id):
    report = get_object_or_404(Report, id=id)
    return render(request, 'main_app/report_detail.html', {'object': report})


def update_report(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'main_app/update_report.html', {'form': form})


def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == 'POST':
        report.delete()
        return redirect('report_list')
    return render(request, 'main_app/report_confirm_delete.html', {'object': report})

def home(request):
    return render(request, 'main_app/home.html')