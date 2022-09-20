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
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()

    # 1. É possivel ajustar os parametros de entrada para especificar o tipo 
    # de dado bem como inserir se o mesmo é ou não um parametro obrigatório, 
    # bem como uma mensagem de erro informando que o campo não pode ser deixado em branco
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

    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists."
                    .format(hotel_id)}, 400

        dados = self.argumentos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados)

        # 3. O ato de salvar um documento pode acarretar também em falha no 
        # processo, para issov para necessario um tratamento utilizando try e 
        # except
        try:
            hotel_obj.save_hotel()
        except:
            # 3. 500 erro interno do servidor
            return {'message': 'An internal error ocurred try to save hotel again'}, 500
        return hotel_obj.json(), 500

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
        
        # 4. O delete demanda a mesma preocupação
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred tryin'}
                    
        return {'message': 'Hotel not found'}, 404