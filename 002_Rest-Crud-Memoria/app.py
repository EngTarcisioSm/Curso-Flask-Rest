from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

app = Flask(__name__)
api = Api(app)

api.add_resource(Hoteis, '/hoteis')

#2. É inserido aqui o nome recurso, como o proximo parametro deve ser uma string
# é colocado <string>:holtel_id
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')


if __name__ == '__main__':

    app.run(debug=True)
