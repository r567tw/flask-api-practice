import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import StoreModel
from schemas import StoreSchema


store = Blueprint("stores", __name__, description="Store")


@store.route("/stores/<string:id>")
class Store(MethodView):
    @store.response(200, StoreSchema)
    def get(self, id):
        return StoreModel.query.get_or_404(id)
        

@store.route("/stores")
class StoreList(MethodView):
    @store.arguments(StoreSchema)
    @store.response(201, StoreSchema)
    def post(self, data):
        newstore = StoreModel(**data)
        try:
            db.session.add(newstore)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="error")
        return newstore, 201

    @store.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
