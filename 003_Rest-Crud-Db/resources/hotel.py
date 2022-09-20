from flask_restful import Resource, reqparse
from models.hotelModel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro',
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina',
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Santa Catarina',
    }
]


class Hoteis(Resource):

    def get(self):

        return {'hoteis': hoteis}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    # 3. Esse método se tornará legado, devido a toda informação agora
    # ser direcionada ao banco de dados.
    # 4. Ir para models/hotelModel
    def findHotel(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):

        hotel = self.findHotel(hotel_id)
        if hotel is not None:
            return hotel, 200
        return {'message': 'Hotel not found'}, 404

    # 1. Será modificado para a utilização do banco de dados
    def post(self, hotel_id):

        # 2. É feito a checagem antes de colocar o hotel se ele já existe caso
        # positivo é retornado uma mensagem de erro, e valor de retorno 400
        # indicando bad request
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists."
                    .format(hotel_id)}, 400

        dados = self.argumentos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados)

        # 9. A transformação do objeto em um json bem como a inclusão dele em 
        # uma lista se tornou legado devido ao uso do banco de dados presente 
        # agora no projeto
        # novo_hotel = hotel_obj.json()
        # hoteis.append(novo_hotel)

        # 10.o metodo save_hotel, salva o hotel no banco de dados. No 
        # SQLAlchemy a ideia de quando há uma nova inserção é que ele é salvo 
        # e não criado ("apenas a ideia") 
        hotel_obj.save_hotel()
        # 11. Indo para /models/hotelModels.py

        # 14. Retorna um Json do Hotel criado 
        return hotel_obj.json(), 200

    def put(self, hotel_id):

        dados = self.argumentos.parse_args()

        hotel_obj = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_obj.json()

        hotel = self.findHotel(hotel_id)
        print(type(hotel))
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted'}
