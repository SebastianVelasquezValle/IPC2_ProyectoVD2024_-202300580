import os
from xml.etree import ElementTree as ET

from controllers.adminController import preCargarXML
from flask import Blueprint, request, jsonify
from models.Imagen import Imagen
from models.matrizDispera.matrizDispersa import MatrizDispersa
from models.Pixel import Pixel

#Creando el blueprint
BlueprintUsuario = Blueprint('usuario', __name__)

#RUTA: http://localhost:4000/usuario/galeria
#aqui va el endpoint


#RUTA: http://localhost:4000/usuario/carga/:id_usuario
@BlueprintUsuario.route('/usuario/carga/<string:id_usuario>', methods=['POST'])
def cargarImagen(id_usuario):
    
    lista_imagenes = preCargarXMLImagenes()

    try:
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'mensaje': 'No se recibió el archivo XML',
                'status': 400
            }), 400

        root = ET.fromstring(xml_entrada)
        #crear la matriz
        matriz = MatrizDispersa()
        nombre = ''
        pixeles = []
        id = len(lista_imagenes) + 1
        for hijo in root:
            if hijo.tag == 'nombre':
                nombre = hijo.text
            elif hijo.tag == 'diseño':
                for pixel in hijo:
                    fila = int(pixel.attrib['fila'])
                    columna = int(pixel.attrib['col'])
                    color = pixel.text
                    #1. lo insertamos en nuestra matriz
                    matriz.insertar(fila,columna,color)
                    #2. Creamos el objeto pixel
                    nuevo_pixel = Pixel(fila,columna,color)
                    pixeles.append(nuevo_pixel)
        
        #3. Creamos el objeto imagen
        nueva_imagen = Imagen(id, id_usuario, nombre, pixeles)
        lista_imagenes.append(nueva_imagen)
        crearXML(lista_imagenes)
        return jsonify({
            'mensaje': 'Imagen cargada correctamente',
            'matriz': matriz.graficar(),
            'status': 200
            }), 200
    
    except:
        return jsonify({
            'message': 'Error al cargar la imagen',
            'status': 404
        }), 404


'''
Acá abajo esta las funciones que no son endpoints
'''
def crearXML(imagenes):
    #si existe el archivo, se elimina
    if os.path.exists('database/imagenes.xml'):
        os.remove('database/imagenes.xml')
    
    #CREAR EL XML
    tree = ET.Element('imagenes')
    for imagen in imagenes:
        imagen:Imagen
        editado = 0
        if imagen.editado == True:
            editado = 1
        imagen_xml = ET.SubElement(tree, 'imagen', id=str(imagen.id), id_usuario=str(imagen.id_usuario), editado=str(editado))
        nombre_xml = ET.SubElement(imagen_xml, 'nombre')
        nombre_xml.text = imagen.nombre
        diseño_xml = ET.SubElement(imagen_xml, 'diseño')
        for pixel in imagen.pixeles:
            pixel:Pixel
            pixel_xml = ET.SubElement(diseño_xml, 'pixel', fila=str(pixel.fila), col=str(pixel.columna))
            pixel_xml.text = pixel.color
    
    tree = ET.ElementTree(tree)

    ET.indent(tree, space='\t', level=0)

    tree.write('database/imagenes.xml', encoding='utf-8', xml_declaration=True)

def preCargarXMLImagenes():
    if not os.path.exists('database/imagenes.xml'):
        return []
    
    #creamos una lista de imagenes
    imagenes = []

    tree = ET.parse('database/imagenes.xml')
    root = tree.getroot()
    for imagen in root:
        id = int(imagen.attrib['id'])
        id_usuario = imagen.attrib['id_usuario']
        editado = imagen.attrib['editado']
        if editado == '1':
            editado = True
        elif editado == '0':
            editado = False
        nombre = ''
        pixeles = []
        for hijo in imagen:
            if hijo.tag == 'nombre':
                nombre = hijo.text
            elif hijo.tag == 'diseño':
                for pixel in hijo:
                    fila = int(pixel.attrib['fila'])
                    columna = int(pixel.attrib['col'])
                    color = pixel.text
                    nuevo_pixel = Pixel(fila,columna,color)
                    pixeles.append(nuevo_pixel)
        
        nueva_imagen = Imagen(id,id_usuario, nombre, pixeles)
        nueva_imagen.editado = editado
        imagenes.append(nueva_imagen)
    
    return imagenes