from django.urls import path
from . import views

urlpatterns = [
    path('complaint/new/', views.register_complaint, name='register_complaint'),
    path('complaints/', views.my_complaints, name='my_complaints'),
    path('admin-panel/complaints/', views.all_complaints, name='all_complaints'),
    path('admin-panel/complaints/<int:complaint_id>/assign/', views.assign_staff, name='assign_staff'),
    path('staff/complaint/<int:complaint_id>/update/', views.update_complaint_status, name='update_status'),

]
