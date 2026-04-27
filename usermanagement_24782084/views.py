from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import CitizenRegisterForm


# ======================
# HOME
# ======================
def home(request):
    return render(request, 'home.html')


# ======================
# REGISTER
# ======================
def register_citizen(request):
    if request.method == 'POST':
        form = CitizenRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registrasi berhasil! Silakan login.")
            return redirect('login')
        else:
            print(form.errors)

    else:
        form = CitizenRegisterForm()

    return render(request, 'register.html', {'form': form})


# ======================
# LOGIN
# ======================
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("DEBUG:", username, password)

        user = authenticate(request, username=username, password=password)

        print("USER:", user)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'login.html')


# ======================
# LOGOUT
# ======================
def custom_logout(request):
    logout(request)
    return redirect('login')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("INPUT:", username, password)

        user = authenticate(request, username=username, password=password)

        print("HASIL AUTH:", user)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print("LOGIN GAGAL")
    
    return render(request, 'login.html')