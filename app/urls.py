from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register_create/', views.RegisterCreateView.as_view(), name='register_create'),
    path('login/', views.LoginCreateView.as_view(), name='login'),
    path('send_code/', views.send_verification_code, name='send_code'),
    path('verify_code/', views.verify_code, name='verify_code'),  # Изменили путь на verify_code
]
