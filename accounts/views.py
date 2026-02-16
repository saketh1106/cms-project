from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from complaints.models import Complaint
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            elif user.groups.filter(name='Staff').exists():
                return redirect('staff_dashboard')

            else:
                return redirect('user_dashboard')

        else:
            return render(request, 'accounts/user_login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/user_login.html')


def staff_login(request):
    # staff also uses SAME logic
    return user_login(request)


def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('staff_dashboard')

        return render(request, 'accounts/staff_login.html', {
            'error': 'Invalid staff credentials'
        })

    return render(request, 'accounts/staff_login.html')

from complaints.models import Complaint

@login_required
def user_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)

    total = complaints.count()
    pending = complaints.filter(status='Pending').count()
    in_progress = complaints.filter(status='In Progress').count()
    solved = complaints.filter(status='Solved').count()

    return render(request, 'accounts/user_dashboard.html', {
        'complaints': complaints,
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'solved': solved
    })




@login_required
def staff_dashboard(request):
    return render(request, 'accounts/staff_dashboard.html')


@login_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

def home(request):
    return render(request, 'accounts/home.html')

from django.contrib.auth.models import User

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        return redirect('user_login')

    return render(request, 'accounts/register.html')


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def admin_dashboard(request):
    total = Complaint.objects.count()
    pending = Complaint.objects.filter(status='Pending').count()
    solved = Complaint.objects.filter(status='Solved').count()
    in_progress = Complaint.objects.filter(status='In Progress').count()

    return render(request, 'accounts/admin_dashboard.html', {
        'total': total,
        'pending': pending,
        'solved': solved,
        'in_progress': in_progress
    })

from django.contrib.auth.decorators import login_required
from complaints.models import Complaint

@login_required
def staff_dashboard(request):
    complaints = Complaint.objects.filter(assigned_staff=request.user)

    return render(request, 'accounts/staff_dashboard.html', {
        'complaints': complaints
    })

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('user_login')
