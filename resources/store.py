import uuid
from flask import request
from flask.views import MethodView
from db import stores
from flask_smorest import abort, Blueprint

from schemas import StoreSchema


store = Blueprint("stores", __name__, description="Store")


@store.route("/stores/<string:id>")
class Store(MethodView):
    @store.response(200, StoreSchema)
    def get(self, id):
        try:
            return stores[id]
        except KeyError:
            abort(404, message="Store is not found")


@store.route("/stores")
class StoreList(MethodView):
    @store.arguments(StoreSchema)
    @store.response(201, StoreSchema)
    def post(self, data):
        store_id = uuid.uuid4().hex
        newstore = {**data, "id": store_id}
        stores[store_id] = newstore
        return newstore, 201

    @store.response(200, StoreSchema(many=True))
    def get(self):
        return {"stores": list(stores.values())}
