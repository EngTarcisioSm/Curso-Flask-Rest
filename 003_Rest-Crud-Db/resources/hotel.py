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
    # 1. O método query.all() retorna todo o banco de dados, utilizando list 
    # comprehension torna-se possivel o fatiamento dos dados seguido de sua 
    # conversão para json 
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


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
        hotel_obj = HotelModel.find_hotel(hotel_id)
        if hotel_obj:
            return hotel_obj.json(), 200
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists."
                    .format(hotel_id)}, 400

        dados = self.argumentos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados)

        hotel_obj.save_hotel()

        return hotel_obj.json(), 200

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

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted'}
        
        return {'message': 'Hotel not found'}, 404