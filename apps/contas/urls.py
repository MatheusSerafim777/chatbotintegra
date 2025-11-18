from django.urls import path

from contas import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
]
