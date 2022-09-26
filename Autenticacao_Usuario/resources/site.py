# 1. Import necessário para o recurso
from flask_restful import Resource
from models.siteModel import SiteModel

# 2. Criação da classe Recurso Sites, que retorna tudo


class Sites(Resource):

    # 3. A principio o get retornará todos os hoteis
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

# 3. Criação da classe Recurso Site que retorna as pesquisas bem como outros
# processos como inclusão, pesquisa e delete


class Site(Resource):
    def get(self, url):
        # 4. buscará um site, aquele passado pela url
        site = SiteModel.find_site(url)
        # 5. se encontrar o site retorna o site caso contrario retorna uma
        # mensagem informando o erro somado a isso o valor 404 indicando "not
        # found" no http
        if site:
            return site.json()
        return {'message': 'Site not found'}, 404

    def post(self, url):
        # 6. O post serve para a criação de um novo site, antes de efetuar sua
        # criação o mesmo é verificado se já não existe, caso exista é
        # retornado uma mensagem de erro informando que este ja existe
        # juntamente com o valor 400 informando uma "bad request". Caso o
        # site não exista é criado e retornado seu json()
        if SiteModel.find_site(url):
            return {"message": "The site '{}' already exists."}, 400

        # 7. Cria o site
        site = SiteModel(url)
        # 8. tenta efetuar o salvamento da alteração no banco de dados
        try:
            site.save_site()
        except:
            # 9. Retorna uma mensagem de erro a respeito da impossibilidade de
            # atualizar o banco de dados com o novo dado inserindo, fazendo
            # com que dessa forma o site não quebre por algum eventual erro no
            # banco de dados
            return {'message': ' An internal error ocurred trying to create a \
            new site.'}, 500

        # 10. caso tudo de certo é retornado o json() do site criado
        return site.json()

    def delete(self, url):
        # 11. para deletar um site é necessário verificar primeiro sua
        # existencia, caso exista o processo pode ser efetuado, caso contrário
        # deve ser retornado uma mensagem de erro
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'Site deleted'}
        return {'message': 'Site not found'}, 404
