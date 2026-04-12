<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm

# READ
def home(request):
    reports = Report.objects.all()
    return render(request, 'main_app/home.html', {'reports': reports})

# CREATE
def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm()
    return render(request, 'main_app/add_report.html', {'form': form})

# UPDATE
def update_report(request, id):
    report = get_object_or_404(Report, id=id)
    form = ReportForm(request.POST or None, instance=report)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'main_app/update_report.html', {'form': form})

# DELETE
def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    report.delete()
    return redirect('home')
=======
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from .models import Report


# ================== LIST (READ) ==================
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'


# ================== DETAIL ==================
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


# ================== CREATE ==================
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')


# ================== UPDATE ==================
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')


# ================== DELETE ==================
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')


# ================== UPDATE STATUS (WORKFLOW) ==================
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('report_list')
>>>>>>> 8426490 (Labsession4)
