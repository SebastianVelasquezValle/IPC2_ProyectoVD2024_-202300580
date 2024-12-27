from django.urls import path, include
from . import views
#Aqui crearemos nuestras propias urls/rutas

urlpatterns = [
    #path='' == http://localhost:8000/
    #path='hola/' == http://localhost:8000/hola/
    path('', views.index, name="index"),
    path('login/', views.loginPage, name="login"),
    path('signin/', views.iniciarSesion, name='signin'),
    path('admin/', views.adminPage, name='admin'),
    path('user/', views.userPage, name='user'),
]