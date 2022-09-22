from flask_restful import Resource, reqparse
from models.hotelModel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


# 1. será criado uma função para a normalização de uma string para consulta sql
# . nesta função existem parametros default. A função tem como objeto principal 
# avaliar se foi ou não recebido cidade, pois é o unico parametro que não 
# existe um valor default válido

def normalize_path_params(cidade=None, 
                          estrelas_min=0, 
                          estrelas_max=0, 
                          diaria_min=0, 
                          diaria_max=99999999999, 
                          limit=50, 
                          offset=0, 
                          **dados):
    
    # 2. se cidade existe é retornado todos os dados, caso não retorna todos 
    # menos o dado cidade
    if cidade:
        # 3. retorna um dicionario
        return {
            'cidade': cidade,
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset
        }
    # 3. Caso cidade não exista retorna tudo menos cidade
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset
    }
        
        
class Hoteis(Resource):
    def get(self):
        dados = path_params.parse_args()

        dados_validos = {chave:dados[chave] for chave in dados if dados[chave]\
            is not None}

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