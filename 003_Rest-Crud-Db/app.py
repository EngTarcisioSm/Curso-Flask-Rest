from re import A
from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

app = Flask(__name__)
# 5. definição do caminho e do nome do banco de dados. O banco de dados será
# criado na raiz da pasta do projeto. Seu nome é banco.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

# 6. configuração para não sobrecarregar a aplicação
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 7. ir para o arquivo hotelModel.py

api = Api(app)

# 4. Criação do banco de dados antes da primeira requisição


@app.before_first_request
def create_db():
    banco.create_all()


api.add_resource(Hoteis, '/hoteis')

api.add_resource(Hotel, '/hoteis/<string:hotel_id>')


if __name__ == '__main__':

    # 3. Veio de sql_alchemy.py --> inicializado o banco de dados aqui. É
    # chamado o import aqui para não haver recursividade na chamada e
    # gerar sobrecarga
    from sql_alchemy import banco
    banco.init_app(app)

    app.run(debug=True)
