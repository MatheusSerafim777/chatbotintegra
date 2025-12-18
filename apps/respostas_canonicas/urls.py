from django.urls import path

from respostas_canonicas import views

urlpatterns = [
    path(
        '',
        views.RespostasCanonicasView.as_view(),
        name='curadoria',
    ),
    path(
        'cadastro_canonica/',
        views.CadastrarCanonicaView.as_view(),
        name='cadastro_canonica',
    ),
    path(
        '<int:id_canonica>/excluir/',
        views.ExcluirCanonicaView.as_view(),
        name='excluir_canonica',
    ),
    path(
        '<int:id_canonica>/editar/',
        views.EditarCanonicaView.as_view(),
        name='editar_canonica',
    ),
]
