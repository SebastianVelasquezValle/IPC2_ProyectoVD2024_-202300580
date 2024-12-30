import os
from xml.etree import ElementTree as ET

from flask import Blueprint, request, jsonify
from controllers.adminController import preCargarXML

#Creando el blueprint
BlueprintAuth = Blueprint('auth', __name__)

#RUTA: http://localhost:4000/login
@BlueprintAuth.route('/login', methods=['POST'])
def login():
    '''
    JSON DE ENTRADA
    {
        'id': id del usuario,
        'password': contraseña del usuario
    }
    '''
    
    lista_usuarios = preCargarXML()
    
    id = request.json['id']
    password = request.json['password']

    if id == 'admin' and password == 'admin':
        return jsonify({
            'message':'Bienvenido admin',
            'rol':1,
            'accion': True,
            'status': 200
        })

    for usuario in lista_usuarios:
        if usuario.id == id and usuario.password == password:
            return jsonify({
                'message': 'Bienvenido '+usuario.nombre,
                'rol':2,
                'accion': True,
                'status': 200
                }),200
    
    return jsonify({
        'message': 'Credenciales invalidas',
        'rol':0,
        'accion': False,
        'status': 200
        }),200