import os
from xml.etree import ElementTree as ET

from flask import Blueprint, request, jsonify
from models.Usuario import Usuario

#Creando el blueprint
BlueprintAdmin = Blueprint('admin', __name__)

#RUTA: http://localhost:4000/admin/cargarUsuarios
@BlueprintAdmin.route('/cargarUsuarios', methods=['POST'])
def cargarUsuarios():
    pass


'''
Acá abajo esta las funciones que no son endpoints
'''
def preCargarXML():
    #Si no existe el archivo, retorna una lista vacia
    if not os.path.exists('database/usuarios.xml'):
        return []
    
    #creamos una lista de usuarios
    usuarios = []

    tree = ET.parse('database/usuarios.xml')
    root = tree.getroot()
    for usuario in root:
        id = usuario.attrib['id']
        pwd = usuario.attrib['pwd']
        nombre = ''
        correo = ''
        telefono = ''
        direccion = ''
        perfil = ''
        for hijo in usuario:
            if hijo.tag == 'NombreCompleto':
                nombre = hijo.text
            elif hijo.tag == 'CorreoElectronico':
                correo = hijo.text
            elif hijo.tag == 'NumeroTelefono':
                telefono = hijo.text
            elif hijo.tag == 'Direccion':
                direccion = hijo.text
            elif hijo.tag == 'perfil':
                perfil = hijo.text
        
        #creamos un objeto usuario
        nuevo_usuario = Usuario(id,pwd,nombre, correo, telefono, direccion, perfil)
        usuarios.append(nuevo_usuario)
    
    return usuarios