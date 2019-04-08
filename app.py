import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from Resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from Resources.Item import Item, Items
from Resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
api = Api(app)
app.secret_key = 'debroop'

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'error': 'Token Expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'Signature Verification Failed'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'Authorization Required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'error': 'Fresh Token Required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'error': 'Token Revoked'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

"""if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)"""
