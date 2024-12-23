import os
from xml.etree import ElementTree as ET

from flask import Blueprint, request, jsonify
from models.Usuario import Usuario

#Creando el blueprint
BlueprintUsuario = Blueprint('usuario', __name__)

# Creamos el login del usuario
#Ruta: http://localhost:4000/usuario/login
@BlueprintUsuario.route('/usuario/login', methods=['POST'])
def login():
    lista_usuario = []
    
    id = request.json['id']
    password = request.json['password']
    
    for usuario in lista_usuario:
        if usuario.id == id and usuario.password == password:
            return jsonify({
                'message': 'Usuario autenticado',
                'accion': True,
                'status': 200
            }),200
    
    return jsonify({
        'message': 'Usuario invalido',
        'accion': False,
        'status': 200
    }),200



'''
Acá abajo esta las funciones que no son endpoints
'''
def validarUsuario(id, lista_usuario):
    for usuario in lista_usuario:
        if usuario.id == id:
            return True
    return False
