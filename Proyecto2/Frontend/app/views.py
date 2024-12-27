import json

import requests
#para el cache
from django.core.cache import cache
#para las cookies
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import LoginForm

# Create your views here.

endpoint = 'http://localhost:4000/'

#Esta es una vista de ejemplo, pero puedes agregar las que necesites
def index(request):
    return render(request, 'index.html')

def loginPage(request):
    return render(request, 'login.html')

def iniciarSesion(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                #Obtenemos losa datos del formulario
                iduser = form.cleaned_data['iduser']
                password = form.cleaned_data['password']

                #PETICION AL BACK
                #ENDPOINT + URL
                url = endpoint + 'login'
                #DATA QUE VOY A ENVIAR
                data = {
                    'id': iduser,
                    'password': password
                }

                #convertimos el diccionario data a json
                json_data = json.dumps(data)

                #HEADERS
                headers = {
                    'Content-Type': 'application/json',
                }

                #llamamos a la peticion Backend
                response = requests.post(url, data=json_data, headers=headers)

                respuesta = response.json()

                #obtener el rol
                rol = int(respuesta['rol'])
                usuario_a_loguearse = iduser
                pagina_redireccion = None
                #IR A ADMIN
                if rol == 1:
                    #Si yo quiero almacenar el usuario en cache
                    #cache.set('id_user', usuario_a_loguearse, timeout=None)
                    #Si quiero almacenarlo en la cookies
                    #pagina_redireccion = redirect('carga') # habilitar cuando se tenga la vista de carga
                    pagina_redireccion = redirect('admin')
                    pagina_redireccion.set_cookie('id_user', iduser)
                    return pagina_redireccion
                elif rol == 2:
                    #Si yo quiero almacenar el usuario en cache
                    #cache.set('id_user', usuario_a_loguearse, timeout=None)
                    #Si quiero almacenarlo en la cookies
                    pagina_redireccion = redirect('user')
                    pagina_redireccion.set_cookie('id_user', iduser)
                    return pagina_redireccion
                else:
                    return render(request, 'login.html')
            
            return render(request, 'login.html')
    except:
        return render(request, 'login.html')

def adminPage(request):
    return render(request, 'admin.html')

def userPage(request):
    return render(request, 'usuario.html')