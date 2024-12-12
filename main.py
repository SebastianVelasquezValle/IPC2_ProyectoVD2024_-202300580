import tkinter as Tk

global id_logueado # VARIABLE GLOBAL PARA SABER SI HAY UN USUARIO LOGUEADO
# En la funciones si quiere modificarlo debo de colocar global id_logueado, pero si lo quiero leer no es necesario poner global

class Login(Tk.Tk):
    def __init__(self):
        super().__init__() #Tk.Tk.__init__(self) o tambien super().__init__()
        self.title("Login")
        #self.geometry("400x500+150+50")
        self.center_window(600,400)
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
        
        username = self.entry_user.get() # OBTENEMOS EL TEXTO DE LOS CAMPOS, CON EL SELF ACLARAMOS QUE SON ATRIBUTOS DE LA CLASE
        passw = self.entry_pass.get() # OBTENEMOS EL TEXTO DE LOS CAMPOS
        
        #print(f"Usuario: {username}, Contraseña: {passw}")
        if username == "admin" and passw == "admin":
            print("Bienvenido Admin")
            
            # LIMPIAMOS LOS CAMPOS
            self.entry_user.delete(0, Tk.END)
            self.entry_pass.delete(0, Tk.END)
            
            # INSTANCIAMOS EL MENU
            adminMenu = MenuAdmin()
            adminMenu.mainloop()
            
        elif username.startswith("ART-") and passw == "123":
            print(f"Bienvenido Artista {username}")
            id_logueado = username
            
            # LIMPIAMOS LOS CAMPOS
            self.entry_user.delete(0, Tk.END)
            self.entry_pass.delete(0, Tk.END)
            
            # INSTANCIAMOS EL MENU
            artistaMenu = MenuArtista()
            artistaMenu.mainloop()
            
        elif username.startswith("IPC-") and passw == "123":
            print(f"Bienvenido Solicitante {username}")
            id_logueado = username
            
            # LIMPIAMOS LOS CAMPOS
            self.entry_user.delete(0, Tk.END)
            self.entry_pass.delete(0, Tk.END)
            
            # INSTANCIAMOS EL MENU
            solicitanteMenu = MenuSolicitantes()
            solicitanteMenu.mainloop()
            
        else:
            print("Usuario o Contraseña incorrectos")
        

    def center_window(self, width, height):
        # Obtén la resolución de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcula la posición
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Establece la geometría con la posición calculada
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    
class MenuAdmin(Tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Admin")
        self.geometry("400x500+150+50")
        
        
        
class MenuArtista(Tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Artista")
        self.geometry("800x500+150+50")
        
class MenuSolicitantes(Tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Solicitante")
        self.geometry("800x500+150+50")

if __name__ == "__main__":
    app = Login()
    app.mainloop()