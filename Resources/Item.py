from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    fresh_jwt_required,
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity
    )

from Models.Item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="field cannot be empty")
    parser.add_argument('store_id', type=int, required=True, help="Store_id mandatory")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message": "row not found"}

    @jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return{"message": "An item with name '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "an error occurred"}, 500
        return item.json(), 201

    @fresh_jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'admin privilege required'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item Deleted"}

    @jwt_required
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class Items(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [x.json() for x in ItemModel.find_all()]

        if user_id:
            return {'items': items}, 200

        return {'items': [item['name'] for item in items],
                'message': 'Login to access prices'}, 200
