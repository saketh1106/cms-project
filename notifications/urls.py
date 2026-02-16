from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:complaint_id>/', views.chat_view, name='chat'),
]
