from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
# noinspection PyUnresolvedReferences
from security import authenticate, identity
# noinspection PyUnresolvedReferences
from Resources.user import UserRegister
# noinspection PyUnresolvedReferences
from Resources.Item import Item, Items
# noinspection PyUnresolvedReferences
from Resources.store import Store, StoreList

app = Flask(__name__)
api = Api(app)
app.secret_key = 'debroop'
jwt = JWT(app, authenticate, identity)  #/auth
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
