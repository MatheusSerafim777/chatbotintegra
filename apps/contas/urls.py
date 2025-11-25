from django.urls import path

from contas import views

urlpatterns = [
    path('entrar/', views.LoginView.as_view(), name='entrar'),
    path('cadastrar/', views.CadastroView.as_view(), name='cadastrar'),
    path('sair/', views.SairView.as_view(), name='sair'),
]
