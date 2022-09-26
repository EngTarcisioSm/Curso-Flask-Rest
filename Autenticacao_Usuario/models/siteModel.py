from sql_alchemy import banco

# 1. Criação do modelo para o banco de dados Site


class SiteModel(banco.Model):

    __tablename__ = 'sites'

    # 2. será criado automaticamente de forma incremental
    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    # 10. Inserir o relacionamento entre SiteModel e HotelModel. Desta forma 
    # define-se que siteModel possui uma relação com hotelModel
    hoteis = banco.relationship('HotelModel')

    # 11. Ao observar que a classe hotelModel possui uma chave estrangeira 
    # para sites, ou seja, todas os objetos criados hotel, terá um site_id 
    # referenciado. O sistema automaticamente irá saber  que a relação é de um 
    # site para muitos hoteis 

    # 12. hoteis recerá uma lista de objetos hoteis que possui a relação com o 
    # site 

    def __init__(self, url) -> None:

        # 3. site_id não é passado pois é criado dinamicamente
        self.url = url

    def json(self):
        # 4. é desejavel também que ao solicitar o json do site cadastrado 
        # seja retornado todos hoteis pertencentes a esse site, será inserido 
        # uma lista vazia em hoteis para futura implementação 
        return {
            'site_id': self.site_id,
            'url': self.url,
            # 13. Agora torna-se possivel a indexação de todos hoteis que tem 
            # relação com um site, tornando possivel a visualização dessa 
            # relação 
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    # 5. A pesquisa do site será feita através da url e não pelo id 
    @classmethod
    def find_hotel(cls, url):

        site = cls.query.filter_by(url=url).first()

        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def update_site(self, url):
        self.url = url

    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()
