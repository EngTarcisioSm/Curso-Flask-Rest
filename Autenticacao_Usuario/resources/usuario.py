from flask_restful import Resource, reqparse
from models.usuario import UserModel
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
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists"
                    .format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()

        return {"message": "User create successfully!"}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_acesso = create_access_token(identity=user.user_id)

            return {'acess_token': token_acesso}, 200

        return {'message': 'The username or password is incorrect.'}, 401
