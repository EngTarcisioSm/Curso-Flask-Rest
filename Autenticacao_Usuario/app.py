from re import A
from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin
#13. Adicionando gerenciador de login fornecido pelo JWT e cuidar de toda 
# parte de autenticação
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 15. Adicionando a chave criptográfica que é necessário para que o 
# gerenciador de autenticação funcione corretamente
app.config['JWT_SECRET_KEY'] = 'DontLetMeDown'

api = Api(app)
# 14. instanciando um gerenciador de autenticação passando a aplicação como 
# parametro para ele 
jwt = JWTManager(app)


@app.before_first_request
def create_db():
    banco.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
# 12. Adicionando recurso (endpoint '/login')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':

    from sql_alchemy import banco
    banco.init_app(app)

    app.run(debug=True)
