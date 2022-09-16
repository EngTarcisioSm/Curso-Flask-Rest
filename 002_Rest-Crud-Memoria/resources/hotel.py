#1. É necessário incluir a biblioteca reqparse para poder receber dados de
# requisições
from flask_restful import Resource, reqparse

hoteis = [
    {
        'hotel_id':'alpha',
        'nome':'Alpha Hotel',
        'estrelas':4.3,
        'diaria':420.34,
        'cidade':'Rio de Janeiro',
    },
    {
        'hotel_id':'bravo',
        'nome':'Bravo Hotel',
        'estrelas':4.4,
        'diaria':380.90,
        'cidade':'Santa Catarina',
    },
    {
        'hotel_id':'charlie',
        'nome':'Charlie Hotel',
        'estrelas':3.9,
        'diaria':320.20,
        'cidade': 'Santa Catarina',
    }
]

class Hoteis(Resource):

    def get(self):

        return {'hoteis': hoteis}

class Hotel(Resource):

    def get(self, hotel_id):

        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel

        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):
        #2. Os dados recebidos ficam alocados dentro de reqparse.RequestParser()
        #o dado de hotel_id não virá como argumento
        argumentos = reqparse.RequestParser()
        #3. Define os argumentos recebidos que serão aceitos, caso sejam enviados
        #outros eses serão descartados na logica do programa.
        argumentos.add_argument('nome')
        argumentos.add_argument('estrelas')
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')

        #4. passara para a variavel dados um conjunto de chave valor conforme
        #os dados especificados acima
        dados = argumentos.parse_args()

        #5. criada a estrutura a ser inserida dentro do "banco de dados" existente
        #hoje que seria hoteis
        novo_hotel = {
            'hotel_id': hotel_id,
            'nome': dados['nome'],
            'estrelas': dados['estrelas'],
            'diaria': dados['diaria'],
            'cidade': dados['cidade']
        }
        hoteis.append(novo_hotel)

        #6. Retorno do hotel criado com o código de sucesso da requisição o
        #código 200
        return novo_hotel, 200

    def put(self):
        pass

    def delete(self):
        pass
