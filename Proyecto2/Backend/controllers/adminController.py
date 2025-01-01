import os
from xml.etree import ElementTree as ET

from controllers.usuarioController import preCargarXMLImagenes
from flask import Blueprint, request, jsonify
from models.Usuario import Usuario

#Creando el blueprint
BlueprintAdmin = Blueprint('admin', __name__)

#RUTA: http://localhost:4000/admin/cargarUsuarios
@BlueprintAdmin.route('/admin/cargarUsuarios', methods=['POST'])
def cargarUsuarios():
    
    lista_usuarios = preCargarXML()
    
    usuariosInvalidos = [] #Lista de usuarios invalidos
    
    try:
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'message': 'Error al cargar los usuarios: EL XML está vacio',
                'status': 404
            }), 404

        root = ET.fromstring(xml_entrada)

        for usuario in root:
            id = usuario.attrib['id']
            if validarRepetido(id, lista_usuarios):
                continue
            pwd = usuario.attrib['pwd']
            nombre = ''
            correo = ''
            telefono = ''
            direccion = ''
            perfil = ''
            for hijos in usuario:
                if hijos.tag == 'NombreCompleto':
                    nombre = hijos.text
                elif hijos.tag == 'CorreoElectronico':
                    correo = hijos.text
                elif hijos.tag == 'NumeroTelefono':
                    telefono = hijos.text
                elif hijos.tag == 'Direccion':
                    direccion = hijos.text
                elif hijos.tag == 'perfil':
                    perfil = hijos.text
                    
            if validarIDUsuario(id) or validarCorreo(correo) or validarTelefono(telefono):
                #print('Usuario no valido')
                usuariosInvalidos.append({
                    'id': id,
                    'correo': correo,
                    'telefono': telefono,
                })
                continue

            nuevo_usuario = Usuario(id,pwd,nombre,correo,telefono,direccion, perfil)
            lista_usuarios.append(nuevo_usuario)
        crearXML(lista_usuarios)
        return jsonify({
            'mensaje':'Usuarios cargados con éxito',
            'usuarios_invalidos': usuariosInvalidos,
            'status':201
        }),201

    except:
        return jsonify({
            'message': 'Error al cargar los usuarios',
            'status': 404
        }), 404

#RUTA: http://localhost:4000/admin/json
@BlueprintAdmin.route('/admin/json', methods=['GET'])
def getUsuariosJSON():
    lista_usuarios = preCargarXML()
    usuarios = []
    for usuario in lista_usuarios:
        user = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'correo': usuario.correo,
            'telefono': usuario.telefono,
            'direccion': usuario.direccion,
            'perfil': usuario.perfil
        }
        usuarios.append(user)
    
    return jsonify({
        'usuarios': usuarios,
        'status': 200
    }),200

#RUTA: http://localhost:4000/admin/xml
@BlueprintAdmin.route('/admin/xml', methods=['GET'])
def getUsuariosXML():
    lista_usuarios = preCargarXML()
    tree = ET.Element('usuarios')
    for usuario in lista_usuarios:
        #2. Creamos un elemento usuario
        usuario_xml = ET.SubElement(tree, 'usuario', id=usuario.id, pwd=usuario.password)
        #3. Creamos los elementos hijos
        nombre = ET.SubElement(usuario_xml, 'NombreCompleto')
        nombre.text = usuario.nombre
        correo = ET.SubElement(usuario_xml, 'CorreoElectronico')
        correo.text = usuario.correo
        telefono = ET.SubElement(usuario_xml, 'NumeroTelefono')
        telefono.text = usuario.telefono
        direccion = ET.SubElement(usuario_xml, 'Direccion')
        direccion.text = usuario.direccion
        perfil = ET.SubElement(usuario_xml, 'perfil')
        perfil.text = usuario.perfil
        imagenes = ET.SubElement(usuario_xml, 'imagenes')
    
    ET.indent(tree, space='\t', level=0)
    xml_str = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
    return xml_str

#RUTA: http://localhost:4000/admin/estadistica
@BlueprintAdmin.route('/admin/estadistica', methods=['GET'])
def estadistica():
    lista_usuarios = preCargarXML()
    lista_imagenes = preCargarXMLImagenes()
    
    data_retornar = []
    '''
    {
        'id usuario': ...
        'imagenes': int
    }
    '''
    
    for usuario in lista_usuarios:
        id_usuario = usuario.id
        contador = 0
        for imagen in lista_imagenes:
            if imagen.id_usuario == id_usuario:
                contador += 1
        
        data = {
            'id_usuario': id_usuario,
            'imagenes': contador
        }
        data_retornar.append(data)
    
    top1, top2, top3 = top3Usuarios(data_retornar)
    data_top = []
    data_top.append(top1)
    data_top.append(top2)
    data_top.append(top3)
    
    
    return jsonify({
        'data': data_retornar,
        'top': data_top,
        'status':200
    }),200


'''
Acá abajo esta las funciones que no son endpoints
'''

def validarRepetido(id, lista_usuarios):
    for usuario in lista_usuarios:
        if usuario.id == id:
            return True
    return False

def validarIDUsuario(id):
    if id.startswith('IPC-') and id[4:].isdigit():
        #print('ID valido')
        return False
    #print('ID invalido')
    return True

def validarCorreo(correo):
    if correo.endswith('.com') and '@' in correo:
        #print('Correo valido')
        return False
    #print('Correo invalido')
    return True

def validarTelefono(telefono):
    if telefono.isdigit() and len(telefono) == 8:
        #print('Telefono valido')
        return False
    #print('Telefono invalido')
    return True

def top3Usuarios(data):
    top = []
    for dato in data:
        # Inserta el dato en la lista top y luego ordena por imágenes (mayor a menor)
        top.append(dato)
        top = sorted(top, key=lambda x: x['imagenes'], reverse=True)
        
        # Limita la lista a solo los tres primeros elementos
        if len(top) > 3:
            top.pop()  # Elimina el último elemento si la lista tiene más de 3
    
    # Si no hay suficientes datos, completa con None
    while len(top) < 3:
        top.append(None)
    
    return top[0], top[1], top[2]

'''
PERSISTENCIA
    XML PARA PERSISTENCIA DE DATOS: database/usuarios.xml
    1. CREAR XML: CADA VEZ QUE SE EDITE, O SE AGREGUE UN NUEVO DATO LLAMAMOS A ESTA FUNCION
    2. PRE-CARGAR XML: CARGA EL XML DE LA DATABABASE Y LO GUARDA EN UNA LISTA
'''

def crearXML(usuarios):
    #Si existe el archivo, se elimina
    if os.path.exists('/database/usuarios.xml'):
        os.remove('/database/usuarios.xml')
    
    #CREAMOS EL XML
    #1. Creamos el elemento raiz
    tree = ET.Element('usuarios')
    for usuario in usuarios:
        #2. Creamos un elemento usuario
        usuario_xml = ET.SubElement(tree, 'usuario', id=usuario.id, pwd=usuario.password)
        #3. Creamos los elementos hijos
        nombre = ET.SubElement(usuario_xml, 'NombreCompleto')
        nombre.text = usuario.nombre
        correo = ET.SubElement(usuario_xml, 'CorreoElectronico')
        correo.text = usuario.correo
        telefono = ET.SubElement(usuario_xml, 'NumeroTelefono')
        telefono.text = usuario.telefono
        direccion = ET.SubElement(usuario_xml, 'Direccion')
        direccion.text = usuario.direccion
        perfil = ET.SubElement(usuario_xml, 'perfil')
        perfil.text = usuario.perfil
    
    #4. Creamos el arbol
    tree = ET.ElementTree(tree)
    #5. Agregamos formato de identacion
    ET.indent(tree, space='\t', level=0)
    #6. Escribimos el arbol en el archivo xml
    tree.write('database/usuarios.xml', encoding='utf-8', xml_declaration=True)

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