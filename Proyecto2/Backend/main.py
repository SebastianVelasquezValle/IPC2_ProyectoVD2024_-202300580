from flask import Flask
from flask_cors import CORS
from controllers.usuarioController import BlueprintUsuario
from controllers.authController import BlueprintAuth
from controllers.adminController import BlueprintAdmin

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(BlueprintUsuario)
app.register_blueprint(BlueprintAuth)
#app.register_blueprint(BlueprintAdmin)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)