from sql_alchemy import banco


class HotelModel(banco.Model):

    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade) -> None:

        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }

    # 4. O modelo do banco se torna responsavel por um método que busca no
    # banco se ja existe algum determinado dado
    # 5. É utilizado o decorador @classmethod para indicar que esse método
    # pode ser utilizado sem que antes uma classe tenha sido instanciada,
    # é necessário a utilização de cls nos seus atributos. 'cls' é a
    # abreviação da classe, sendo uma palavra chave
    @classmethod
    def find_hotel(cls, hotel_id):
        # 6. query é um método que existe dentro da classe que hotelModel
        # herdou, significando "consulta", será filtrado através de filter_by
        # realizando a operação "SELECT * FROM hoteis WHERE hotel_id=hotel_id"
        # .first() retorna a primeira visualização de hotel_id que for
        # encontrado

        # 7. a utilização de "query", "filter_by" e "first" simplifica o acesso
        # ao banco de dados, não necessitando efetuar vários processos,
        # efetuando o acesso de forma bem simplificada o acesso ao db
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()

        # 8. Se existe o hotel, será retornado o hotel caso contrario será
        # retornado None
        if hotel:
            return hotel
        return None

        # 9. retornando para hotel.py

    # 11. Criando o método para salvar o dado recebido
    def save_hotel(self):
        # 12. É aberto uma conexão com o banco e salvo os dados do objeto. 
        # Nota que não é necessário passar os dados a serem salvos, uma vez 
        # que em outra parte do código foi criado um objeto com esses dados. O 
        # método abaixo tem a automação de reconhecer os dados que necessitam 
        # de serem salvos no banco de dados quando a função save_hotel for 
        # chamada.
        banco.session.add(self)
        # 13. Commita a inclusão feita no banco 
        banco.session.commit()
