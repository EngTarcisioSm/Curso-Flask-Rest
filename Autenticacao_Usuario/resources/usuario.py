from xmlrpc.client import boolean
from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The \
            'login' field cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The \
            'password' field cannot be left blank")
# 4. inserir mais este campo a ser capturado ao receber a requisição, não sendo obrigatorio seu preenchimento
atributos.add_argument('ativado', type=boolean)


class User(Resource):

    def get(self, user_id):
        user_obj = UserModel.find_user(user_id)
        if user_obj:
            return user_obj.json(), 200
        return {'message': 'User not found'}, 404

    @jwt_required()
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
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists"
                    .format(dados['login'])}

        user = UserModel(**dados)
        # 5. para garantir que nenhum usuario malicioso efetue a ativação
        # enviando true, será forçado aqui o valor de ativado para false para
        # que não ocorra problemas com a logica implementada
        user.ativado = False

        user.save_user()

        return {"message": "User create successfully!"}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            # 6. alem da checagem acima de verificar se o usuario e senha
            # estão iguais, será verificado também aqui se o usuario teve sua
            # conta ativada
            if user.ativado:
                token_acesso = create_access_token(identity=user.user_id)
                return {'acess_token': token_acesso}, 200
            return {'message': 'User not confirmed.'}, 400
        return {'message': 'The username or password is incorrect.'}, 401


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']

        BLACKLIST.add(jwt_id)

        return {'message': 'Logout successfully!'}, 200


# 7. Criação de um recurso que efetua a ativação do usuario
class UserConfirm(Resource):

    # 8. Será um método de classe, não necessitando criar um usuário
    @classmethod
    def get(cls, user_id):
        # 9. tenta localizar o usuario atraves do id
        user = UserModel.find_user(user_id)

        if not user:
            return {'message': "User id '{}' not found.".format(user_id)}, 404

        # 10. passo pelo if de cima logo usuario foi encontrado devendo ser
        # ativado
        user.ativado = True
        # 11. Atualizando o status do usuario
        user.save_user()
        return {'message': "User id '{}' confirmed successfully."
                .format(user_id)}
