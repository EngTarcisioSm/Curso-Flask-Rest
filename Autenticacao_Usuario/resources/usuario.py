from flask_restful import Resource, reqparse
from models.usuario import UserModel

class User(Resource):

    def get(self, user_id):
        user_obj = UserModel.find_hotel(user_id)
        if user_obj:
            return user_obj.json(), 200
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_hotel(user_id)

        if user:
            try:
                user.delete_hotel()
            except:
                return {'message': 'An error ocurred tryin'}
        return {'message': 'user not found'}, 404

