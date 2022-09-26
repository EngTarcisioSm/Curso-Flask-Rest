from sql_alchemy import banco


class SiteModel(banco.Model):

    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    def __init__(self, url) -> None:

        self.url = url

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):

        site = cls.query.filter_by(url=url).first()

        if site:
            return site
        return None

    # 5. criado o metodo de pesquisa de ID
    @classmethod
    def find_by_id(cls, site_id):

        site = cls.query.filter_by(site_id=site_id).first()

        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def update_site(self, url):
        self.url = url

    def delete_site(self):
        # 1. antes de deletar o site é necessário deletar todos os hoteis
        # presentes naquele site

        # 2. utilizando compreensão de listas é pego os objeto armazenados em
        # hoteis e utilizado seu metodo delete, com isso todos os hoteis
        # associados aquele site serão deletados
        [hotel.delete_hotel() for hotel in self.hoteis]

        banco.session.delete(self)
        banco.session.commit()
