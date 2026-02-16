from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Complaint

@login_required
def register_complaint(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Complaint.objects.create(
            title=title,
            description=description,
            user=request.user
        )

        return redirect('my_complaints')

    return render(request, 'complaints/register_complaint.html')


@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'complaints/my_complaints.html', {
        'complaints': complaints
    })

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def all_complaints(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaints/all_complaints.html', {
        'complaints': complaints
    })

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

@staff_member_required
def assign_staff(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    staff_users = User.objects.filter(groups__name='Staff')

    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        complaint.assigned_staff = User.objects.get(id=staff_id)
        complaint.status = 'In Progress'
        complaint.save()
        return redirect('all_complaints')

    return render(request, 'complaints/assign_staff.html', {
        'complaint': complaint,
        'staff_users': staff_users
    })

@login_required
def update_complaint_status(request, complaint_id):
    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        assigned_staff=request.user
    )

    if request.method == 'POST':
        complaint.status = request.POST.get('status')
        complaint.save()
        return redirect('staff_dashboard')

    return render(request, 'complaints/update_status.html', {
        'complaint': complaint
    })
