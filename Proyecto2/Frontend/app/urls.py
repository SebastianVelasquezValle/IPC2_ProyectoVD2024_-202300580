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
    path('admin/carga/', views.cargaAdminPage, name='carga'),
    path('admin/cargaxml/', views.cargarXML, name='cargaxml'),
    path('admin/cargausers/', views.enviarUsersXML, name='cargausers'),
    path('admin/users/', views.verUsuariosPage, name='users'),
    path('admin/usersxml/', views.verUsuariosXMLPage, name='usersxml'),
    path('admin/estadisticas/', views.statsPage, name='estadisticas'),
    path('logout/', views.cerrarSesion, name='logout'),
    path('user/crear/', views.crearPage, name='crear'),
    path('user/cargarxml/', views.cargarXMLDisenio, name='cargarxml'),
    path('user/cargadisenio/', views.enviarDisenio, name='cargadisenio'),
    path('user/ayuda/', views.ayuda, name='ayuda'),
    path('user/editar/', views.editarPage, name='editar'),
    path('user/editarimagen/', views.editarImagen, name='editarimagen'),
    path('user/galeria/', views.galeriaPage, name='galeria'),
]