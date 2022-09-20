from flask_restful import Resource, reqparse
# 1. importando o banco de dados de usuarios
from models.usuario import UserModel

# 2. não haverá necessidade de acesso a todos os usuários
# class Hoteis(Resource):

#     def get(self):
#         return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


# 3. Criação da classe (recurso) usuário
class User(Resource):

    # 4. em user haverá get e delete, não sendo necessário um parse de requisições
    # argumentos = reqparse.RequestParser()

    # argumentos.add_argument('nome', type=str, required=True, help="The name \
    #     field cannot be left blank.")
    # argumentos.add_argument('estrelas', type=float, required=True, help="The \
    #     'estrelas' field cannot be left brank")
    # argumentos.add_argument('diaria')
    # argumentos.add_argument('cidade')

    # 6. Modificação do método get e do metodo delete
    def get(self, user_id):
        user_obj = UserModel.find_hotel(user_id)
        if user_obj:
            return user_obj.json(), 200
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_hotel(user_id)

        if user:
            try:
                user.delete_hotel()
            except:
                return {'message': 'An error ocurred tryin'}
        return {'message': 'user not found'}, 404

    # 5. Não existiram os metodos post e delete neste recurso
    # def post(self, hotel_id):

    #     if HotelModel.find_hotel(hotel_id):
    #         return {"message": "Hotel id '{}' already exists."
    #                 .format(hotel_id)}, 400

    #     dados = self.argumentos.parse_args()
    #     hotel_obj = HotelModel(hotel_id, **dados)

    #     try:
    #         hotel_obj.save_hotel()
    #     except:
    #         return {'message': 'An internal error ocurred try to save hotel again'}, 500
    #     return hotel_obj.json(), 500

    # def put(self, hotel_id):

    #     dados = self.argumentos.parse_args()

    #     hotel_encontrado = HotelModel.find_hotel(hotel_id)

    #     if hotel_encontrado:

    #         hotel_encontrado.update_hotel(**dados)
    #         hotel_encontrado.save_hotel()

    #         return hotel_encontrado.json(), 200

    #     hotel_new = HotelModel(hotel_id, **dados)
    #     hotel_new.save_hotel()
    #     return hotel_new.json(), 201
