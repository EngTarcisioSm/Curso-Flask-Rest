
from flask_restful import Resource, reqparse
from models.hotelModel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3
from resources.filtros import normalize_path_params
from resources.filtros import CONSULTA_COM_CIDADE
from resources.filtros import CONSULTA_SEM_CIDADE

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
        connection = sqlite3.connect('Autenticacao_Usuario/banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()

        dados_validos = {chave: dados[chave] for chave in dados if dados[chave]
                         is not None}

        parametros = normalize_path_params(**dados_validos)

        if parametros.get('cidade'):
            consulta = CONSULTA_COM_CIDADE
            tupla = tuple([parametros[chave] for chave in parametros])
        else:
            consulta = CONSULTA_SEM_CIDADE
            tupla = tuple([parametros[chave] for chave in parametros])

        resultado = cursor.execute(consulta, tupla)

        hoteis = list()

        for linha in resultado:
            hoteis.append({
                "hotel_id": linha[0],
                "nome": linha[1],
                "estrelas": linha[2],
                "diaria": linha[3],
                "cidade": linha[4],
                # 2. incluir o Id do site em que o hotel esta associado 
                "site_id": linha[5]
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
    # 1. Adição do argumento novo a ser pego site_id, atributo obrigatório, 
    # sendo do tipo int, obrigatório e tendo uma mensagem de erro configurada 
    # para o caso de não receber o valor que necessita de forma apropriada 
    argumentos.add_argument('site_id', type=int, required=True, 
        help='Every hotel needs to be linked with a site')

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
