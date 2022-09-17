from flask_restful import Resource, reqparse

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

    # 3. Como o metodo put necessita também de inserir novos valores baseados
    # em valores recebidos algumas linhas de put são externadas, em questão
    # aquelas que formam a estrutura que retira os dados desejados da
    # estrutura recebida
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    # 1. O metodo put exige que seja verifica se o hotel já existe, essa logica
    # já é implementada no metodo get, o trecho em que essa checagem é retirada
    # do metodo get, criado um novo metodo que atenda tanto ao metodo get
    # quanto ao métod put
    def findHotel(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    # 2. O método get foi modificado, retirando de si a checagem, pois a mesma
    # será utilizada pelo metodo put
    def get(self, hotel_id):

        hotel = self.findHotel(hotel_id)
        if hotel is not None:
            return hotel, 200
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):

        dados = self.argumentos.parse_args()
        # 4. dados é uma estrutura que apresenta conjuntos de chave valor
        # atraves de **kargs ele é desempacotado dentro de novo hotel
        novo_hotel = {'hotel_id': hotel_id, **dados}
        hoteis.append(novo_hotel)

        return novo_hotel, 200

    def put(self, hotel_id):

        # 5.
        dados = self.argumentos.parse_args()
        novo_hotel = {'hotel_id': hotel_id, **dados}

        hotel = self.findHotel(hotel_id)
        print(type(hotel))
        if hotel:
            # 6. Atualiza hotel
            hotel.update(novo_hotel)
            return novo_hotel, 200
        # 7. Caso não exista ele é inserido, é retornado o valor 201 indicando
        # que foi criado novo valor dentro do banco de dados
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self):
        pass
