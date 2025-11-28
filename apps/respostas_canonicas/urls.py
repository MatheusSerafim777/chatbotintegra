from django.urls import path

from respostas_canonicas import views

urlpatterns = [
    path('', views.CuradoriaView.as_view(), name='curadoria'),
    path('cadastro_canonica/', views.CadastrarCanonicaView.as_view(), name='cadastro_canonica')
]