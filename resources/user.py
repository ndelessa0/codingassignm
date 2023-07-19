from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models.user import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank.')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank.')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400

        user = UserModel(username=data['username'], password=generate_password_hash(data['password']))
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank.')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank.')

    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials.'}, 401
