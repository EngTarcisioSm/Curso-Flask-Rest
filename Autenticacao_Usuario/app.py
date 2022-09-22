from re import A
# 16. importar o modulo para gerar json de resposta para o logout
from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
# 10. inserindo a classe/recurso de deslogar
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontLetMeDown'
# 12. ativar o blacklist nas configurações
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

# 13. cria função com propósito de verificar se um token esta na black list,
# isso é efetuado utilizando um decorador que da essa função a função criada
# tendo como função verificar se um token esta na blacklist

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST


# 14. revoga o acesso a uma token que entrou e esta na blacklist
@jwt.revoked_token_loader
def token_de_acesso_invalidado(self, token):
    # 15. converte o dicionario para json informando que o usuario foi 
    # deslogado caso seu token esteja na blacklist, retornando não autorizado 
    # "401"
    return jsonify({'message': 'You have been logged out!'}), 401


@app.before_first_request
def create_db():
    banco.create_all()


api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
# 11. criando o recurso para efetuar o deslogar da aplicação
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':

    from sql_alchemy import banco
    banco.init_app(app)

    app.run(debug=True)
