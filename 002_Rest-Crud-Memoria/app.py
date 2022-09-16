#1. imports de bibliotecas necessárias para criação de rest api
from flask import Flask
from flask_restful import Resource, Api

#2. criação de objetos
app = Flask(__name__)
api = Api(app)

#3. cada classe é um recurso da rest api
class Hoteis(Resource):

    #4. cada recurso deve implementar os metodos do http
    def get(self):

        #5. resultado da requisição get, retorna o dicionário
        return {'hoteis': 'meus hoteis'}

#6. adicionando o recurso a api, '/hoteis' é como esse recurso deve ser chamado
api.add_resource(Hoteis, '/hoteis')


if __name__ == '__main__':
    #execução da aplicação em modo de debug
    app.run(debug=True)
