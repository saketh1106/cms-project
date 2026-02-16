from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from complaints.models import Complaint
from .models import Message

@login_required
def chat_view(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    # RULE: staff can chat only if assigned & not solved
    if request.user.groups.filter(name='Staff').exists():
        if complaint.assigned_staff != request.user or complaint.status == 'Solved':
            return redirect('staff_dashboard')

    messages = Message.objects.filter(complaint=complaint).order_by('timestamp')

    if request.method == 'POST':
        text = request.POST.get('text')

        # decide receiver
        if request.user == complaint.user:
            receiver = complaint.assigned_staff
        else:
            receiver = complaint.user

        Message.objects.create(
            complaint=complaint,
            sender=request.user,
            receiver=receiver,
            text=text
        )

        return redirect('chat', complaint_id=complaint.id)

    return render(request, 'notifications/chat.html', {
        'complaint': complaint,
        'messages': messages
    })

