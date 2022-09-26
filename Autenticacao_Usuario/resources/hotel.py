
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


def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=10,
                          diaria_min=0,
                          diaria_max=99999999999,
                          limit=50,
                          offset=0,
                          **dados):

    if cidade:
        return {
            'cidade': cidade,
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset
        }
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
        connection = sqlite3.connect('Autenticacao_Usuario/banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()

        dados_validos = {chave: dados[chave] for chave in dados if dados[chave]
                         is not None}

        parametros = normalize_path_params(**dados_validos)

        if parametros.get('cidade'):

            # 1. Foi substituido na pesquisa o simbolo de ">" por ">=" e o 
            # simbolo de "<" por "<=" para que a consulta tivesse uma 
            # abrangencia mais proxima da realidade do que se deseja
            consulta = "SELECT * FROM hoteis \
                WHERE cidade = ? \
                and (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) \
                LIMIT ? OFFSET ?"
            tupla = tuple([parametros[chave] for chave in parametros])
        else:
            # 2. Foi substituido aqui também os simbolos de pesquisa ">" por 
            # ">=" e "<" e "<=" para uma melhor pesquisa
            consulta = "SELECT * FROM hoteis WHERE \
                (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) \
                LIMIT ? OFFSET ?"
            tupla = tuple([parametros[chave] for chave in parametros])

        resultado = cursor.execute(consulta, tupla)

        hoteis = list()

        for linha in resultado:
            hoteis.append({
                "hotel_id": linha[0],
                "nome": linha[1],
                "estrelas": linha[2],
                "diaria": linha[3],
                "cidade": linha[4]
            })
        

        return {'hoteis': hoteis}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()

    argumentos.add_argument('nome', type=str, required=True, help="The name \
        field cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True, help="The \
        'estrelas' field cannot be left brank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    # def findHotel(self, hotel_id):
    #     for hotel in hoteis:
    #         if hotel['hotel_id'] == hotel_id:
    #             return hotel
    #     return None

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
