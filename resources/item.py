import uuid
from flask import request
from flask.views import MethodView
from db import items
from flask_smorest import abort, Blueprint

from schemas import ItemSchema, ItemUpdateSchema


item = Blueprint("items", __name__, description="Item")


@item.route("/items/<string:id>")
class Item(MethodView):
    @item.arguments(ItemUpdateSchema)
    @item.response(200, ItemSchema)
    def put(self, data, id):
        # data = request.get_json()

        try:
            items[id] |= data
            return data
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, id):
        try:
            result = {"deleted": True, **items[id]}
            del items[id]
            return result
        except KeyError:
            abort(404, message="Item not found")


@item.route("/items")
class ItemList(MethodView):
    @item.response(200, ItemSchema(many=True))
    def get(self):
        return list(items.values())

    @item.arguments(ItemSchema)
    @item.response(201, ItemSchema)
    def post(self, data):
        # data = request.get_json()
        id = uuid.uuid4().hex
        item = {"id": id, **data}
        try:
            items[id] = item
            return item
        except KeyError:
            abort(404, message="Item not found")
