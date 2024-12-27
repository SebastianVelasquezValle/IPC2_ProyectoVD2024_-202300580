from django.urls import path, include
from . import views
#Aqui crearemos nuestras propias urls/rutas

urlpatterns = [
    path('', views.index, name="index"),
]