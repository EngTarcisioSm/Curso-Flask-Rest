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

    def post(self, hotel_id):

        dados = self.argumentos.parse_args()
        # 2. Alterada a logica de inserção de novos hoteis com auxilio da
        # classe objeto. É criado o objeto que representa o novo hotel e em
        # seguida é utilizado o método que efetua a conversão
        hotel_obj = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_obj.json()

        hoteis.append(novo_hotel)

        return novo_hotel, 200

    def put(self, hotel_id):

        dados = self.argumentos.parse_args()
        # 3. Alterada a logica de inserção de novos hoteis com auxilio da
        # classe objeto. É criado o objeto que representa o novo hotel e em
        # seguida é utilizado o método que efetua a conversão
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
