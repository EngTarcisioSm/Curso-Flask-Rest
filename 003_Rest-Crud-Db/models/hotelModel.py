# 7. importa o objeto do banco de dados
from sql_alchemy import banco

# 8. passará a herdar de banco.Model


class HotelModel(banco.Model):

    # 9. Determina o nome da tabela
    __tablename__ = 'hoteis'

    # 10. Mapeamento para o SQLAlchemy das colunas existentes dentro da tabela
    # hoteis
    # 11. indica que hoteis_id é uma coluna do tipo string sendo uma chave
    # primaria
    hotel_id = banco.Column(banco.String, primary_key=True)
    # 12. indica que nome é uma coluna do tipo string de tamanho 80
    nome = banco.Column(banco.String(80))
    # 13. indica que estrelas é uma coluna do tipo float com precisão de uma
    # casa decimal
    estrelas = banco.Column(banco.Float(precision=1))
    # 14. indica que diaria é uma coluna do tipo float com precisão de duas
    # casas decimais
    diaria = banco.Column(banco.Float(precision=2))
    # 15. indica que cidade é uma coluna do tipo string com tamanho maximo de
    # 40 digitos
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
