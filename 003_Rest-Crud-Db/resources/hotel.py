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

        # 3. A instancia do novo hotel esta sendo criado sem nem mesmo saber 
        # se existe a necessidade dela 
        # hotel_obj = HotelModel(hotel_id, **dados)
        # novo_hotel = hotel_obj.json()

        # 1. Como é necessário utilizar a busca no banco de dados é utilizado
        # o método para verificar a existencia do hotel com o determinado ID
        # hotel = self.findHotel(hotel_id)
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            # 7. O metodo update_hotel ainda não esta criado, é passado apenas 
            # os "dados" vindos da requisição, uma vez que o seu hotel_id já 
            # existe  
            hotel_encontrado.update_hotel(**dados)
            # 10. As atualizações são salvas no objeto e consequentemente no db
            hotel_encontrado.save_hotel()

            # 2. Retorna o json do hotel encontrado em formato json
            return hotel_encontrado.json(), 200

        # 4. Caso o hotel não exista ele é criado 
        hotel_new = HotelModel(hotel_id, **dados)
        # 5. Salvo o hotel criado
        hotel_new.save_hotel()
        # 6. Retorno do hotel salvo em formato json
        return hotel_new.json(), 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted'}
