import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from db import db
from models import ItemModel 
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema


item = Blueprint("items", __name__, description="Item")


@item.route("/items/<string:id>")
class Item(MethodView):
    @item.arguments(ItemUpdateSchema)
    @item.response(200, ItemSchema)
    def put(self, data, id):
        # data = request.get_json()
        item = ItemModel.query.get_or_404(id)
        item.price = data["price"]
        item.name = data["name"]

        db.session.add(item)
        db.session.commit()
        return item


    def delete(self, id):
        item = ItemModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {'deleted': True}


@item.route("/items")
class ItemList(MethodView):
    @item.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
        # return list(items.values())

    @item.arguments(ItemSchema)
    @item.response(201, ItemSchema)
    def post(self, data):
        item = ItemModel(**data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="error")
        return item
