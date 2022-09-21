from flask_restful import Resource, reqparse
from models.usuario import UserModel
# 11. Importando os modulos de criação de token de acesso e o modulo de
# comparação de strings
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The \
            'login' field cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The \
            'password' field cannot be left blank")


class User(Resource):

    def get(self, user_id):
        user_obj = UserModel.find_user(user_id)
        if user_obj:
            return user_obj.json(), 200
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurred try in'}
        return {'message': 'User deleted'}, 404


class UserRegister(Resource):
    # /cadastro

    def post(self):
        # 5. Tornado esse recurso global devido a essa e a classe UserLogin
        # necessitarem dos mesmos dados
        # atributos = reqparse.RequestParser()
        # atributos.add_argument('login', type=str, required=True, help="The \
        #     'login' field cannot be left blank")
        # atributos.add_argument('senha', type=str, required=True, help="The \
        #     'password' field cannot be left blank")

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists"
                    .format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()

        return {"message": "User create successfully!"}, 201


# 1. Criando um novo método em usuarios para efetuar login atraves de um
# método post, é obtido os dados de login atraves de uma requisição possuindo
# login e senha, após isso é verificado se o usuario existe e se a senha que
# se encontra no sistema é a mesma que foi passada pelo usuario. Os dados
# estando corretos é criado um token de acesso para o usuario efetuar acesso
# para o usuario

# 2. Novo recurso
class UserLogin(Resource):

    # 3. o metodo criado abaixo é um class methodo para não ser necessário sua
    # instanciação sempre que um usuario desejar efetuar login
    @classmethod
    def post(cls):
        # 4. é necessário obter um parse dos atributos que chegam da
        # requisição, como nesta neste mesmo modulo ja existe um procedimento
        # semelhante, entretanto esta em outra classe, a configuração do parte
        # se tornará global do modulo fazendo com que ambas a classes possam-
        # se utilizar dessa configuração
        dados = atributos.parse_args()

        # 6. Efetuando consulta no banco de dados para verificar se o usuario
        # que desejou o login se o mesmo existe
        user = UserModel.find_by_login(dados['login'])

        # 7. É verificado a existencia do usuario e verificado se a string
        # enviada e aquela existente no bando de dados são iguais, essa
        # comparação é efetuada pelo metodo safe_str_comp() por ser mais seguro

        if user and safe_str_cmp(user.senha, dados['senha']):
            # 8. Caso o usuario exista e a senha seja a correta é gerado um
            # token de acesso com base no id do usuario
            token_acesso = create_access_token(identity=user.user_id)

            # 9. È retornado ao usuario o token de acesso juntamento com o
            # valor 200 indicando sucesso na requisição
            return {'acess_token': token_acesso}, 200

        # 10. caso a verifica-se falhe em alguma etapa é enviado uma mensagem
        # de erro juntamente com o código de erro http respectivo de não
        # autorizado
        return {'message': 'The username or password is incorrect.'}, 401
