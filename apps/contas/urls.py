from django.urls import path

from contas import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('sair/', views.SairView.as_view(), name='sair'),
]
