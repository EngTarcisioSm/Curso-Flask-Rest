
#  1. Criando a classe que representa os hoteis, que irá gerar um objeto que os 
# representa


class HotelModel:

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade) -> None:

        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
    
    # 2. Criação de método que gera o json a partir dos atributos 
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }