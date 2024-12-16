class UsuarioLogueado:
    userlogueado = None
    def __init__(self, usuarioLogueado):
        #self.usuarioLogueado = usuarioLogueado
        UsuarioLogueado.userlogueado = usuarioLogueado

    def getUsuarioLogueado(self):
        #return self.usuarioLogueado
        return UsuarioLogueado.userlogueado
    
    def setUsuarioLogueado(self, usuarioLogueado):
        #self.usuarioLogueado = usuarioLogueado
        UsuarioLogueado.userlogueado = usuarioLogueado
        
    def mostrarUsuario(self):
        print(f'Usuario logueado: {self.userlogueado}')
