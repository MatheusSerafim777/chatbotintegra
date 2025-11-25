from django.urls import path

from chat import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('documentos/', views.DocumentosView.as_view(), name='documentos'),
]
