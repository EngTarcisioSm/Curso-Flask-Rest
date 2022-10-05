
from flask_restful import Resource, reqparse
from models.siteModel import SiteModel
from models.hotelModel import HotelModel
from flask_jwt_extended import jwt_required
# 1. alterando a lib de manipulação do banco
import mysql.connector
from models.siteModel import SiteModel
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
        # 2. modificar sqlite3 por "mysql.connector" e o banco de dados
        # passado també deve ser alterado contendo alguns outros argumentos
        # como user, password, host e database
        # connection = sqlite3.connect('Autenticacao_Usuario/banco.db')
        connection = mysql.connector.connect(
            user='brynden2022',
            password='brynden123456',
            host='brynden2022.mysql.pythonanywhere-services.com',
            database='brynden2022$default'
        )
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
        
        # 3. O resultado da pesquisa não é dada na variavem resultado, sendo a 
        # logica no mysql um pouco diferente daquela observada no sqlite3
        # resultado = cursor.execute(consulta, tupla)
        cursor.execute(consulta, tupla)
        resultado = cursor.fetchall()
        hoteis = list()

        # 4. como forma de proteção é necessário avaliar se foi obtido algum 
        # resultado na pesquisa efetuada e tendo sido armazenada na variavel 
        # resultado
        if resultado: 
            for linha in resultado:
                hoteis.append({
                    "hotel_id": linha[0],
                    "nome": linha[1],
                    "estrelas": linha[2],
                    "diaria": linha[3],
                    "cidade": linha[4],
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

        if not SiteModel.find_by_id(dados['site_id']):
            return {'message': 'The hotel must be associated to a valid site id.'}, 400

        try:
            hotel_obj.save_hotel()
        except:
            return {'message': 'An internal error ocurred try to save hotel again'}, 500
        return hotel_obj.json(), 500

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

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred tryin'}

        return {'message': 'Hotel not found'}, 404
