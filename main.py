import tkinter as Tk

global id_logueado # VARIABLE GLOBAL PARA SABER SI HAY UN USUARIO LOGUEADO
# En la funciones si quiere modificarlo debo de colocar global id_logueado, pero si lo quiero leer no es necesario poner global

# Esto es de prueba

from estructuras.lista_simple.listaSimple import ListaSimple

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
        self.destroy() # Cerramos la ventana actual
        app.deiconify() # Mostramos la ventana de login
        #app.quit()
        
class Login(Ventana):
    def __init__(self):
        super().__init__("Login", 600, 400) #Tk.Tk.__init__(self) o tambien super().__init__()
        #self.title("Login"
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
        global id_logueado # INDICAMOS QUE VAMOS A USAR LA VARIABLE GLOBAL
        # POSIBLEMENTE YA NO LO USE PORQUE CREAR UNA CLASE PARA EL ID LOGUEADO
        
        username = self.entry_user.get() # OBTENEMOS EL TEXTO DE LOS CAMPOS, CON EL SELF ACLARAMOS QUE SON ATRIBUTOS DE LA CLASE
        passw = self.entry_pass.get() # OBTENEMOS EL TEXTO DE LOS CAMPOS
        
        if username == "admin" and passw == "admin":
            print("Bienvenido Admin")
            
            # LIMPIAMOS LOS CAMPOS
            self.limpiar_Campos_Login()
            # self.destroy()
            # INSTANCIAMOS EL MENU
            # adminMenu = MenuAdmin()
            # adminMenu.mainloop()
            self.abrirMenu(MenuAdmin)

            
        elif username.startswith("ART-") and passw == "123":
            print(f"Bienvenido Artista {username}")
            id_logueado = username
            
            # LIMPIAMOS LOS CAMPOS
            self.limpiar_Campos_Login()
            #self.withdraw()
            
            # INSTANCIAMOS EL MENU
            # artistaMenu = MenuArtista()
            # artistaMenu.mainloop()
            self.abrirMenu(MenuArtista)

            
        elif username.startswith("IPC-") and passw == "123":
            print(f"Bienvenido Solicitante {username}")
            id_logueado = username
            
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
        #self.geometry("400x500+150+50")
        #self.center_window(800,500)
        self.minsize(600,300)
        self.components()
        
    def components(self):
        # Creamos los botones
        btn_CargarSolicitantes = Tk.Button(self, text="Cargar Solicitantes", font=("Arial", 12))
        btn_CargarSolicitantes.place(relx=0.3, rely=0.3, anchor=Tk.CENTER)
        
        btn_CargarArtistas = Tk.Button(self, text="Cargar Artistas", font=("Arial", 12))
        btn_CargarArtistas.place(relx=0.6, rely=0.3, anchor=Tk.CENTER)
        
        btn_VerSolicitantes = Tk.Button(self, text="Ver Solicitantes", font=("Arial", 12))
        btn_VerSolicitantes.place(relx=0.3, rely=0.5, anchor=Tk.CENTER)
        
        btn_VerArtistas = Tk.Button(self, text="Ver Artistas", font=("Arial", 12))
        btn_VerArtistas.place(relx=0.6, rely=0.5, anchor=Tk.CENTER)
        
        btn_CerrarSesion = Tk.Button(self, text="Cerrar Sesión", font=("Arial", 12), command=self.cerrarSessionMenu)
        btn_CerrarSesion.place(relx=0.7, rely=0.05, anchor=Tk.CENTER)
        
        
class MenuArtista(Ventana):
    def __init__(self):
        super().__init__("Menú Artista", 800, 500)
        #self.title("Menú Artista")
        self.minsize(600,300)
        self.components()
    
    def components(self):
        # Este laberl mostrar quien nos esta mandando una imagen y el nombre de la imagen
        lbl_mensajeDelSolicitante = Tk.Label(self, font=("Arial", 12))
        lbl_mensajeDelSolicitante.config(text=f"Solicitante: {id_logueado} \n\nImagen: ") # Esto falta por configurar
        lbl_mensajeDelSolicitante.place(relx=0.6, rely=0.3, anchor=Tk.CENTER)
        
        btn_Aceptar = Tk.Button(self, text="Aceptar", font=("Arial", 12))
        btn_Aceptar.place(relx=0.3, rely=0.3, anchor=Tk.CENTER)
        
        bnt_VerCola = Tk.Button(self, text="Ver Cola", font=("Arial", 12))
        bnt_VerCola.place(relx=0.3, rely=0.6, anchor=Tk.CENTER)
        
        btn_ImagenesSolicitadas = Tk.Button(self, text="Imágenes Solicitadas", font=("Arial", 12))
        btn_ImagenesSolicitadas.place(relx=0.3, rely=0.7, anchor=Tk.CENTER)
        
        btn_CerrarSesion = Tk.Button(self, text="Cerrar Sesión", font=("Arial", 12), command=self.cerrarSessionMenu)
        btn_CerrarSesion.place(relx=0.7, rely=0.05, anchor=Tk.CENTER)
        
        
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
        self.components()
        
    def components(self):
        # Titulo
        lbl_titulo = Tk.Label(self, text="Solicitar", font=("Arial", 16))
        lbl_titulo.place(relx=0.5, rely=0.1, anchor=Tk.CENTER)
        
        # Boton de solicitar
        btn_CargarFigurar = Tk.Button(self, text="Cargar Figurar", font=("Arial", 12))
        btn_CargarFigurar.place(relx=0.3, rely=0.3, anchor=Tk.CENTER)
        
        btn_Solicitar = Tk.Button(self, text="Solicitar", font=("Arial", 12))
        btn_Solicitar.place(relx=0.3, rely=0.5, anchor=Tk.CENTER)
        
        btn_VerPila = Tk.Button(self, text="Ver Pila", font=("Arial", 12))
        btn_VerPila.place(relx=0.3, rely=0.7, anchor=Tk.CENTER)
        
        btn_VerLista = Tk.Button(self, text="Ver Lista", font=("Arial", 12))
        btn_VerLista.place(relx=0.3, rely=0.9, anchor=Tk.CENTER)
        
        btn_CerrarSesion = Tk.Button(self, text="Cerrar Sesión", font=("Arial", 12), command=self.cerrarSessionMenu)
        btn_CerrarSesion.place(relx=0.9, rely=0.05, anchor=Tk.CENTER)


if __name__ == "__main__":
    app = Login()
    app.mainloop()
