from django.urls import path
from . import views
from .views import create_admin



urlpatterns = [
    path('login/user/', views.user_login, name='user_login'),
    path('login/staff/', views.staff_login, name='staff_login'),
    path('', views.home, name='home'),
    path('register/', views.user_register, name='user_register'),

    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path("create-admin/", create_admin),


]

