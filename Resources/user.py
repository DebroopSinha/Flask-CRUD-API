from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from flask_restful import Resource, reqparse
from Models.user import UserModel
import bcrypt
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help="field cannot be empty")
_user_parser.add_argument('password', type=str, required=True, help="field cannot be empty")


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username((data['username'])):
            return {"message": "Username already in use"}, 400
        p = data['password'].encode('utf-8')
        pw = bcrypt.hashpw(p, bcrypt.gensalt()).encode('utf-8')
        user = UserModel(data['username'], pw)
        user.save_to_db()

        return {"message": "User Created Successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {"message": "User not Found"}, 404

        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {"message": "User Not Found"}, 404

        user.delete_from_db()
        return {"message": "user deleted"}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user:
            p = data['password'].encode('utf-8')
            pw = bcrypt.hashpw(p, user.password)
            if user.password == pw:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            return {'message': 'invalid credentials'}, 401
        return {'message': 'user does not exist'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Logged Out!'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
