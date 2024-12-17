import tkinter as Tk
from tkinter import filedialog
#Element Tree
import xml.etree.ElementTree as ET

#global id_logueado # VARIABLE GLOBAL PARA SABER SI HAY UN USUARIO LOGUEADO
# En la funciones si quiere modificarlo debo de colocar global id_logueado, pero si lo quiero leer no es necesario poner global

from clases.Artista import Artista
from clases.Imagen import Imagen
from clases.Solicitante import Solicitante
from clases.SolicitudCola import SolicitudCola
from clases.SolicitudPila import SolicitudPila
from estructuras.estructuras import (listaSolicitantes, listaArtistas, colaSolicitudes)
from estructuras.matrizDispera.matrizDispersa import MatrizDispersa

from clases.UsuarioLogueado import UsuarioLogueado


class Ventana(Tk.Tk):
    def __init__(self, titulo, witdh, height):
        super().__init__()
        self.title(titulo)
        self.center_window(witdh, height)

    def center_window(self, width, height):
        # Obtén la resolución de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

            # Calcula la posición
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Establece la geometría con la posición calculada
        self.geometry(f"{width}x{height}+{x}+{y}") 
    
    def cerrarSessionMenu(self):
        UsuarioLogueado(None)
        self.destroy() # Cerramos la ventana actual
        app.deiconify() # Mostramos la ventana de login
        #app.quit()
        
class Login(Ventana):
    def __init__(self):
        super().__init__("Login", 600, 400) #Tk.Tk.__init__(self) o tambien super().__init__()
        self.minsize(400,200)
        self.maxsize(800,500)
        self.components()
        
    def components(self):
        # Creamos los label
        lbl_user = Tk.Label(self, text="Usuario", font=("Arial", 12))
        lbl_user.place(relx=0.3, rely=0.4, anchor=Tk.CENTER)
        
        lbl_pass = Tk.Label(self, text="Contraseña", font=("Arial", 12))
        lbl_pass.place(relx=0.3, rely=0.5, anchor=Tk.CENTER)
        
        # Creamos los entry (textFields)
        self.entry_user = Tk.Entry(self, font=("Arial", 12), width=25) # PARA PODER USARLOS FUERA DE LA FUNCION LE PONEMOS
        self.entry_user.place(relx=0.6, rely=0.4, anchor=Tk.CENTER)
        
        self.entry_pass = Tk.Entry(self, font=("Arial", 12), width=25, show="*")
        self.entry_pass.place(relx=0.6, rely=0.5, anchor=Tk.CENTER)
        
        # Creamos los botones
        btn_login = Tk.Button(self, text="Iniciar Sesión", font=("Arial", 12), command=self.verify_login)
        btn_login.place(relx=0.5, rely=0.7, anchor=Tk.CENTER)
        
    def verify_login(self):
        #global id_logueado # INDICAMOS QUE VAMOS A USAR LA VARIABLE GLOBAL
        # POSIBLEMENTE YA NO LO USE PORQUE CREAR UNA CLASE PARA EL ID LOGUEADO
        
        id_user = self.entry_user.get() # OBTENEMOS EL TEXTO DE LOS CAMPOS, CON EL SELF ACLARAMOS QUE SON ATRIBUTOS DE LA CLASE
        passw = self.entry_pass.get() # OBTENEMOS EL TEXTO DE LOS CAMPOS
        
        if id_user == "admin" and passw == "admin":
            print("Bienvenido Admin")
            
            # LIMPIAMOS LOS CAMPOS
            self.limpiar_Campos_Login()
            # self.destroy()
            # INSTANCIAMOS EL MENU
            # adminMenu = MenuAdmin()
            # adminMenu.mainloop()
            self.abrirMenu(MenuAdmin)

            
        elif id_user.startswith("ART-") and listaArtistas.loginUsuario(id_user, passw) == True:
            print(f"Bienvenido Artista {id_user}")
            #id_logueado = id_user
            UsuarioLogueado(id_user)
            # LIMPIAMOS LOS CAMPOS
            self.limpiar_Campos_Login()
            #self.withdraw()
            
            # INSTANCIAMOS EL MENU
            # artistaMenu = MenuArtista()
            # artistaMenu.mainloop()
            self.abrirMenu(MenuArtista)

            
        elif id_user.startswith("IPC-") and listaSolicitantes.login(id_user, passw) == True:
            print(f"Bienvenido Solicitante {id_user}")
            #id_logueado = id_user
            UsuarioLogueado(id_user)
            #print(f"Usuario logueado: {UsuarioLogueado.userlogueado}")
            
            # LIMPIAMOS LOS CAMPOS
            self.limpiar_Campos_Login()
            
            # INSTANCIAMOS EL MENU
            # solicitanteMenu = MenuSolicitantes()
            # solicitanteMenu.mainloop()
            # self.withdraw()
            self.abrirMenu(MenuSolicitantesGaleria)
            
        else:
            print("Usuario o Contraseña incorrectos")
    
    def abrirMenu(self, menu):
        # Abriremos el menu y ocultando el login
        nuevoMenu = menu()
        self.withdraw() # Ocultamos la ventana de login
        nuevoMenu.protocol("WM_DELETE_WINDOW", lambda: self.destruirMenu(nuevoMenu))
        
    def destruirMenu(self, menu):
        # Abre de nuevo la ventana de login si se cierra el menu
        self.deiconify()  # Mostramos la ventana de login
        menu.destroy() # Destruimos la ventana del menu
        
    def limpiar_Campos_Login(self):
        self.entry_user.delete(0, Tk.END)
        self.entry_pass.delete(0, Tk.END)
        
class MenuAdmin(Ventana):
    def __init__(self):
        super().__init__("Menú Admin", 700, 500) #Tk.Tk.__init__(self) o tambien super().__init__()
        #self.title("Menú Admin")
        #self.center_window(800,500)
        self.minsize(600,300)
        self.components()
        
    def components(self):
        # Creamos los botones
        btn_CargarSolicitantes = Tk.Button(self, text="Cargar Solicitantes", font=("Arial", 12))
        btn_CargarSolicitantes.config(command=self.cargarSolicitantes)
        btn_CargarSolicitantes.place(relx=0.3, rely=0.3, anchor=Tk.CENTER)
        
        btn_CargarArtistas = Tk.Button(self, text="Cargar Artistas", font=("Arial", 12))
        btn_CargarArtistas.config(command=self.cargarArtista)
        btn_CargarArtistas.place(relx=0.6, rely=0.3, anchor=Tk.CENTER)
        
        btn_VerSolicitantes = Tk.Button(self, text="Ver Solicitantes", font=("Arial", 12))
        btn_VerSolicitantes.config(command=self.verSolicitantes)
        btn_VerSolicitantes.place(relx=0.3, rely=0.5, anchor=Tk.CENTER)
        
        btn_VerArtistas = Tk.Button(self, text="Ver Artistas", font=("Arial", 12))
        btn_VerArtistas.config(command=self.verArtistas)
        btn_VerArtistas.place(relx=0.6, rely=0.5, anchor=Tk.CENTER)
        
        btn_CerrarSesion = Tk.Button(self, text="Cerrar Sesión", font=("Arial", 12), command=self.cerrarSessionMenu)
        btn_CerrarSesion.place(relx=0.7, rely=0.05, anchor=Tk.CENTER)
        
    def cargarSolicitantes(self):
        ruta = filedialog.askopenfilename(title="Cargar Archivo", filetypes=(('Text files', '*.xml'), ('All files','*.*')))
        #print(f"Ruta: {ruta}")
        
        try:
            #PARSEAR EL XML
            tree = ET.parse(ruta)
            #Obtengo el elemento raiz
            root = tree.getroot()

            if root.tag == "solicitantes":
                for solicitante in root:
                    id = solicitante.attrib["id"]
                    pwd = solicitante.attrib["pwd"]
                    nombre = ''
                    correo = ''
                    telefono = ''
                    direccion = ''
                    for hijo in solicitante:
                        if hijo.tag == "NombreCompleto":
                            nombre = hijo.text
                        elif hijo.tag == "CorreoElectronico":
                            correo = hijo.text
                        elif hijo.tag == "NumeroTelefono":
                            telefono = hijo.text
                        elif hijo.tag == "Direccion":
                            direccion = hijo.text
                            
                    #print(f"ID: {id}, PWD: {pwd}, Nombre: {nombre}, Correo: {correo}, Telefono: {telefono}, Direccion: {direccion}")
                    nuevo_solicitante = Solicitante(id,pwd,nombre,correo,telefono,direccion)
                    listaSolicitantes.insertar(nuevo_solicitante)
        except:
            print("Error al cargar el archivo")
        
        # #PARSEAR EL XML
        # tree = ET.parse(ruta)
        # #Obtengo el elemento raiz
        # root = tree.getroot()

        # if root.tag == "solicitantes":
        #     for solicitante in root:
        #         id = solicitante.attrib["id"]
        #         pwd = solicitante.attrib["pwd"]
        #         nombre = ''
        #         correo = ''
        #         telefono = ''
        #         direccion = ''
        #         for hijo in solicitante:
        #             if hijo.tag == "NombreCompleto":
        #                 nombre = hijo.text
        #             elif hijo.tag == "CorreoElectronico":
        #                 correo = hijo.text
        #             elif hijo.tag == "NumeroTelefono":
        #                 telefono = hijo.text
        #             elif hijo.tag == "Direccion":
        #                 direccion = hijo.text
                        
        #         #print(f"ID: {id}, PWD: {pwd}, Nombre: {nombre}, Correo: {correo}, Telefono: {telefono}, Direccion: {direccion}")
        #         nuevo_solicitante = Solicitante(id,pwd,nombre,correo,telefono,direccion)
        #         listaSolicitantes.insertar(nuevo_solicitante)
                
    def cargarArtista(self):
        ruta = filedialog.askopenfilename(title="Cargar Archivo", filetypes=(('Text files', '*.xml'), ('All files','*.*')))
        
        #print(f"Ruta: {ruta}")
        
        try:
            #PARSEAR EL XML
            tree = ET.parse(ruta)
            # #Obtengo el elemento raiz
            root = tree.getroot()
            if root.tag == "Artistas":
                for artista in root:
                    id = artista.attrib["id"]
                    pwd = artista.attrib["pwd"]
                    nombre = ''
                    correo = ''
                    telefono = ''
                    especialidades = ''
                    notas = ''
                    for hijo in artista:
                        if hijo.tag == "NombreCompleto":
                            nombre = hijo.text
                        elif hijo.tag == "CorreoElectronico":
                            correo = hijo.text
                        elif hijo.tag == "NumeroTelefono":
                            telefono = hijo.text
                        elif hijo.tag == "Especialidades":
                            especialidades = hijo.text
                        elif hijo.tag == "NotasAdicionales":
                            notas = hijo.text

                    #print(f"ID: {id}, PWD: {pwd}, Nombre: {nombre}, Correo: {correo}, Telefono: {telefono}, Especialidades: {especialidades}, Notas: {notas}")
                    nuevo_artista = Artista(id,pwd,nombre,correo,telefono,especialidades,notas)
                    listaArtistas.insertar(nuevo_artista)
        except:
            print("Error al cargar el archivo")
        # #PARSEAR EL XML
        # tree = ET.parse(ruta)
        # # #Obtengo el elemento raiz
        # root = tree.getroot()
        # if root.tag == "Artistas":
        #     for artista in root:
        #         id = artista.attrib["id"]
        #         pwd = artista.attrib["pwd"]
        #         nombre = ''
        #         correo = ''
        #         telefono = ''
        #         especialidades = ''
        #         notas = ''
        #         for hijo in artista:
        #             if hijo.tag == "NombreCompleto":
        #                 nombre = hijo.text
        #             elif hijo.tag == "CorreoElectronico":
        #                 correo = hijo.text
        #             elif hijo.tag == "NumeroTelefono":
        #                 telefono = hijo.text
        #             elif hijo.tag == "Especialidades":
        #                 especialidades = hijo.text
        #             elif hijo.tag == "NotasAdicionales":
        #                 notas = hijo.text

        #         #print(f"ID: {id}, PWD: {pwd}, Nombre: {nombre}, Correo: {correo}, Telefono: {telefono}, Especialidades: {especialidades}, Notas: {notas}")
        #         nuevo_artista = Artista(id,pwd,nombre,correo,telefono,especialidades,notas)
        #         listaArtistas.insertar(nuevo_artista)
    
    def verSolicitantes(self):
        try:
            listaSolicitantes.graficar()
        except:
            print("No hay solicitantes")
        
    def verArtistas(self):
        try:
            listaArtistas.graficar()
        except:
            print("No hay artistas")

class MenuArtista(Ventana):
    def __init__(self):
        super().__init__("Menú Artista", 800, 500)
        #self.title("Menú Artista")
        self.minsize(600,300)
        
        # Este laberl mostrar quien nos esta mandando una imagen y el nombre de la imagen
        #print(f"Usuario logueado: {UsuarioLogueado.userlogueado}")
        self.lbl_mensajeDelSolicitante = Tk.Label(self, font=("Arial", 12))
        #lbl_mensajeDelSolicitante.config(text=f"Solicitante: {} \n\nImagen: ") # Esto falta por configurar
        self.lbl_mensajeDelSolicitante.place(relx=0.6, rely=0.3, anchor=Tk.CENTER)
        
        self.iniciarDatos()
        
        self.components()
        
    def iniciarDatos(self):
        
        if colaSolicitudes.verPrimero() == None:
            self.lbl_mensajeDelSolicitante.config(text=f"No hay solicitudes")
        else:
            solicitud = colaSolicitudes.verPrimero()
            self.lbl_mensajeDelSolicitante.config(text=f"Solicitante: {solicitud.id_solicitante} \n\nImagen: {solicitud.id}")
    
    def components(self):
        #print(F"Usuario logueado: {UsuarioLogueado.userlogueado}")
        
        btn_Aceptar = Tk.Button(self, text="Aceptar", font=("Arial", 12))
        btn_Aceptar.config(command=self.AceptarSolicitud)
        btn_Aceptar.place(relx=0.3, rely=0.3, anchor=Tk.CENTER)
        
        btn_VerCola = Tk.Button(self, text="Ver Cola", font=("Arial", 12))
        btn_VerCola.config(command=self.verCola)
        btn_VerCola.place(relx=0.3, rely=0.6, anchor=Tk.CENTER)
        
        btn_ImagenesSolicitadas = Tk.Button(self, text="Imágenes Solicitadas", font=("Arial", 12))
        btn_ImagenesSolicitadas.config(command=self.verListaCircular)
        btn_ImagenesSolicitadas.place(relx=0.3, rely=0.7, anchor=Tk.CENTER)
        
        btn_CerrarSesion = Tk.Button(self, text="Cerrar Sesión", font=("Arial", 12), command=self.cerrarSessionMenu)
        btn_CerrarSesion.place(relx=0.7, rely=0.05, anchor=Tk.CENTER)
    
    def AceptarSolicitud(self):
        print(f"Usuario logueado: {UsuarioLogueado.userlogueado}")
        
        solicitud = colaSolicitudes.verPrimero()
        if solicitud == None:
            return
        
        #LO SACAMOS DE LA COLA
        solicitud_aceptada = colaSolicitudes.dequeue()
        #INSERTAN EN LA LISTA CIRCULAR
        listaArtistas.insertarProcesados(UsuarioLogueado.userlogueado,solicitud_aceptada)
        
        #GENERAMOS LA FIGURA
        matriz_figura = MatrizDispersa()
        
        #PARSEAR EL XML
        tree = ET.parse(solicitud_aceptada.ruta_xml)
        #Obtengo el elemento raiz
        root = tree.getroot()
        nombre_figura = ''
        for elemento in root:
            if elemento.tag == 'diseño':
                for pixel in elemento:
                    fila = int(pixel.attrib['fila'])
                    columna = int(pixel.attrib['col'])
                    color = pixel.text
                    matriz_figura.insertar(fila,columna,color)
            elif elemento.tag == 'nombre':
                nombre_figura = elemento.text

        #GRAFICAMOS
        ruta = matriz_figura.graficar(solicitud_aceptada.id)
        #creamos el nuevo objeto imagen para insertarlo a la lista doble del usuario
        nueva_imagen = Imagen(solicitud_aceptada.id,nombre_figura,ruta)
        #insertamos el objeto a la lista doble del usuario
        listaSolicitantes.insertarImagenUsuario(solicitud_aceptada.id_solicitante,nueva_imagen)

        self.iniciarDatos()
    
    def verCola(self):
        colaSolicitudes.graficar()
    
    def verListaCircular(self):
        print(f"Usuario logueado: {UsuarioLogueado.userlogueado}")
        artista = listaArtistas.obtenerUsuario(UsuarioLogueado.userlogueado)
        artista.procesadas.graficar()
        
class MenuSolicitantesGaleria(Ventana):
    def __init__(self):
        super().__init__("Menú Solicitante", 800, 500)
        self.minsize(600,300)
        self.components()
        
    def components(self):
        bnt_Anterior = Tk.Button(self, text="Anterior", font=("Arial", 12), bg="#5fd1de", width=20)
        bnt_Anterior.place(relx=0.3, rely=0.15, anchor=Tk.CENTER)
        
        bnt_Siguiente = Tk.Button(self, text="Siguiente", font=("Arial", 12), bg="#5fd1de", width=20)
        bnt_Siguiente.place(relx=0.7, rely=0.15, anchor=Tk.CENTER)
        
        btn_Solicitar = Tk.Button(self, text="Solicitar", font=("Arial", 12), bg="#53e6b2", command=self.solicitarImagen)
        btn_Solicitar.place(relx=0.5, rely=0.15, anchor=Tk.CENTER)
        
        btn_CerrarSesion = Tk.Button(self, text="Cerrar Sesión", font=("Arial", 12), bg="#e84661",command=self.cerrarSessionMenu)
        btn_CerrarSesion.place(relx=0.9, rely=0.05, anchor=Tk.CENTER)
        
    def solicitarImagen(self):
        self.destroy()
        solicitar = MenuSolicitantesSolicitar()
        solicitar.protocol("WM_DELETE_WINDOW", lambda: self.destruirMenu(solicitar))
# La clase redirigira a la ventana de solicitar, con un boton de solicitar
class MenuSolicitantesSolicitar(Ventana):
    def __init__(self):
        super().__init__("Menú Solicitante", 800, 500)
        self.minsize(600,300)
        print(f"Usuario logueado: {UsuarioLogueado.userlogueado}")
        self.solicitante:Solicitante = listaSolicitantes.buscar(UsuarioLogueado.userlogueado)
        # self.solicitante = None
        # self.imagen = None
        print(len(self.solicitante.imagenes))
        #self.DatosIniciados()
        self.components()
        
    def DatosIniciados(self):
        print(f"Usuario logueado: {UsuarioLogueado.userlogueado}")
        self.solicitante:Solicitante = listaSolicitantes.buscar(UsuarioLogueado.userlogueado)
        print(f"Solicitante imagenes: {len(self.solicitante.imagenes) if self.solicitante and self.solicitante.imagenes else 0}")
        
    def components(self):
        # Titulo
        lbl_titulo = Tk.Label(self, text="Solicitar", font=("Arial", 16))
        lbl_titulo.place(relx=0.5, rely=0.1, anchor=Tk.CENTER)
        
        # Boton de solicitar
        btn_CargarFigurar = Tk.Button(self, text="Cargar Figurar", font=("Arial", 12))
        btn_CargarFigurar.config(command=self.cargarXMLFiguras)
        btn_CargarFigurar.place(relx=0.3, rely=0.3, anchor=Tk.CENTER)
        
        btn_Solicitar = Tk.Button(self, text="Solicitar", font=("Arial", 12))
        btn_Solicitar.config(command=self.Solicitar)
        btn_Solicitar.place(relx=0.3, rely=0.5, anchor=Tk.CENTER)
        
        btn_VerPila = Tk.Button(self, text="Ver Pila", font=("Arial", 12))
        btn_VerPila.config(command=self.VerPila)
        btn_VerPila.place(relx=0.3, rely=0.7, anchor=Tk.CENTER)
        
        btn_VerLista = Tk.Button(self, text="Ver Lista Doble", font=("Arial", 12))
        btn_VerLista.config(command=self.VerLista)
        btn_VerLista.place(relx=0.3, rely=0.9, anchor=Tk.CENTER)
        
        btn_CerrarSesion = Tk.Button(self, text="Cerrar Sesión", font=("Arial", 12), command=self.cerrarSessionMenu)
        btn_CerrarSesion.place(relx=0.9, rely=0.05, anchor=Tk.CENTER)
    
    def VerPila(self):
        self.solicitante.pila.graficar() 
        # if self.solicitante and self.solicitante.pila:
        #     self.solicitante.pila.graficar()
        # else:
        #     print("No hay solicitudes")
        #     self.solicitante.pila.graficar() # para revisar si en realidad no hay solicitudes
            
        
    def VerLista(self):
        pass
        
    def ImagenActual(imagen):
        print(f'Nombre: {imagen.nombre}')
        print(f'Ruta Imagen: {imagen.ruta_imagen}')
        print(f'ID: {imagen.id}')
        
    def cargarXMLFiguras(self):
        # ruta = filedialog.askopenfilename(title="Cargar Archivo", filetypes=(('Text files', '*.xml'), ('All files','*.*')))
        try:
            ruta = filedialog.askopenfilename(title="Cargar Archivo", filetypes=(('Text files', '*.xml'), ('All files','*.*')))
            #PARSEAR EL XML
            tree = ET.parse(ruta)
            #Obtengo el elemento raiz
            root = tree.getroot()

            id = ''
            if root.tag == "figura":
                for elementos in root:
                    if elementos.tag == "nombre":
                        id = elementos.attrib["id"]
            
            nueva = SolicitudPila(id,ruta)
            listaSolicitantes.insertaraPilaUsuario(UsuarioLogueado.userlogueado,nueva)
            print("Solicitud agregada")
            
            #self.DatosIniciados()
            
        except:
            print("Error al cargar el archivo")
            
        #print(len(self.solicitante.imagenes))
        # if len(self.solicitante.imagenes) != 0:
        #     self.imagen:Imagen = self.solicitante.imagenes.primero.valor
        #     print("Si se")
        
    def Solicitar(self):
        valorSacado = listaSolicitantes.sacardePilaUsuario(UsuarioLogueado.userlogueado)
        while valorSacado != None:
            nueva_solicitud = SolicitudCola(valorSacado.id,valorSacado.ruta_xml,UsuarioLogueado.userlogueado)
            colaSolicitudes.enqueue(nueva_solicitud)
            valorSacado = listaSolicitantes.sacardePilaUsuario(UsuarioLogueado.userlogueado)

if __name__ == "__main__":
    app = Login()
    app.mainloop()
    