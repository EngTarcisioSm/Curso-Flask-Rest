from flask_restful import Resource, reqparse
from models.usuario import UserModel


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


# 1. Será criado um novo recurso referente ao cadastro de usuario
class UserRegister(Resource):
    # /cadastro

    # 2. O cadastro será feito através do método post, desta forma é necessário
    # efetuar um parse dos dados recebidos o usuario
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="The \
            'login' field cannot be left blank")
        atributos.add_argument('senha', type=str, required=True, help="The \
            'password' field cannot be left blank")

        # 3. pegando apenas os atributos necessários
        dados = atributos.parse_args()

        # 4. Antes de criar o usuario é necessário saber se aquele usuario
        # "login" ja existe, logo é necessário efetuar uma verificação
        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists"
                    .format(dados['login'])}

        # 5. Caso o usuario não exista o processo de criação é dado o devido
        # prosseguimento
        user = UserModel(**dados)
        user.save_user()

        # 6. É retornado mesagem e o código 201 de created
        return {"message": "User create successfully!"}, 201
