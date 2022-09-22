from flask_restful import Resource, reqparse
from models.hotelModel import HotelModel

from flask_jwt_extended import jwt_required
# 3. Como a pesquisa existe uma complexidade maior é necessário importar 
# biblioteca específica para tratar de requisições 
import sqlite3


# 1. os dados de pesquisa são passado via path baseado no caractere inicial "?"
#  para iniciar o corpo da pesquisa dentro do path, juntamente com o caractere 
# "&" para indicar uma junção de mais de uma pesquisa como se fosse um "E"

# 2. Será criado um reqparse especifico para a pesquisa.  

# 4. Criando o req parser
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):

    def get(self):

        # 5. Serão recebidos todos os dados vindos do path
        dados = path_params.parse_args()

        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()

    argumentos.add_argument('nome', type=str, required=True, help="The name \
        field cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True, help="The \
        'estrelas' field cannot be left brank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def findHotel(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel_obj = HotelModel.find_hotel(hotel_id)
        if hotel_obj:
            return hotel_obj.json(), 200
        return {'message': 'Hotel not found'}, 404

    @jwt_required()
    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists."
                    .format(hotel_id)}, 400

        dados = self.argumentos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados)

        try:
            hotel_obj.save_hotel()
        except:
            return {'message': 'An internal error ocurred try to save hotel again'}, 500
        return hotel_obj.json(), 500

    # 4. ==3
    @jwt_required()
    def put(self, hotel_id):

        dados = self.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:

            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()

            return hotel_encontrado.json(), 200


        hotel_new = HotelModel(hotel_id, **dados)
        hotel_new.save_hotel()
        return hotel_new.json(), 201

    # 5. ==3
    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred tryin'}
                    
        return {'message': 'Hotel not found'}, 404