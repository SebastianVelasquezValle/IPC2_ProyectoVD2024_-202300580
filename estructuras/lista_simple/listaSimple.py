import os
from estructuras.lista_simple.nodo import Nodo

class ListaSimple:
    def __init__(self):
        self.primero = None
        self.tamanio = 0
        
    def __len__(self):
        return self.ultimo
    
    def insertar(self, valor):
        
        # Crear un nuevo nodo
        nuevo = Nodo(valor)

        # VERIFICAMOS SI LA LISTA ESTA VACIA
        if self.primero == None:
            self.primero = nuevo # Asignamos el nuevo nodo al primero
        else:
            actual = self.primero # Nodo actual, el cual sera un puntero
            while actual != None:
                if actual.siguiente == None: # Si el nodo siguiente es nulo
                    actual.siguiente = nuevo # Asignamos el nuevo nodo al siguiente
                    break
                actual = actual.siguiente # Avanzamos al siguiente nodo, si es que no es nulo
        self.tamanio+=1
        
    def imprimirLista(self):
        actual = self.primero # Nodo actual, el cual sera un puntero
        while actual != None:
            print(str(actual.valor))
            actual = actual.siguiente # Avanzamos al siguiente nodo, si es que no es nulo el siguiente 
            
    
    def obtenerUsuario(self,id):
        actual = self.primero
        while actual != None:
            if actual.valor.id == id: # Si el valor.id (o sea el id del valor/es ingresados) del nodo actual es igual al id
                return actual.valor
            actual = actual.siguiente
        return None
    
    def validarExiste(self,id):
        actual = self.primero
        while actual != None:
            if actual.valor.id == id:
                return True
            actual = actual.siguiente
        return False
    
    def graficar(self):
        codigodot = ''
        codigodot += '''digraph G {
    rankdir=LR;
    node[shape=record, height=.1]
    '''
        contador_nodos = 1

        #CREAR LOS NODOS
        actual = self.primero
        while actual != None:
            codigodot += 'nodo'+str(contador_nodos)+'[label=\"{'+str(actual.valor)+'|<f1>}\"];\n'
            contador_nodos+=1
            actual = actual.siguiente
        
        #CREAR LOS ENLACES
        actual = self.primero
        contador_nodos = 1
        while actual.siguiente != None:
            codigodot += 'nodo'+str(contador_nodos)+' -> nodo'+str(contador_nodos+1)+';\n'
            contador_nodos+=1
            actual = actual.siguiente
        
        codigodot += '}'

        #ESCRIBIR EL TEXTO CONCATENASO AL ARCHIVO DOT
        #defino la ruta donde se guarda el codigo dot
        ruta_dot = 'reportesdot/listaSimple.dot'
        #creamos el archivo dot
        archivo = open(ruta_dot,'w')
        #escribimos el archivo
        archivo.write(codigodot)
        #cerramos el archivo
        archivo.close()

        # GENERACIÓN DE LA IMAGEN
        
        #defino la ruta donde se guarda la imagen
        ruta_imagen = 'reportes/listaSimple.png'
        #defino el comando de graphviz para compilar el dot y generar la imagen
        comando = 'dot -Tpng '+ ruta_dot + ' -o ' + ruta_imagen
        #ejecuto el comando
        os.system(comando)

        # ABRIR LA IMAGEN

        #1. CONVERTIMOS LA RUTA RELATIVA A UNA RUTA ABSOLUTA
        # RUTA RELATIVA: ./hola.txt
        # RUTA ABSOLUTA: C://users/equis/documents/hola.txt
        ruta_abrir_imagen = os.path.abspath(ruta_imagen)
        os.startfile(ruta_abrir_imagen)
        print('grafico generado con exito')