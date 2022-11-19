import uuid
from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import db
from models import UserModel
from schemas import UserSchema

from flask_jwt_extended import create_access_token



user = Blueprint("users", __name__ , description="User")

@user.route('/register')
class UserRegister(MethodView):

    @user.arguments(UserSchema)
    def post(self, userData):
        user = UserModel(**userData)
        db.session.add(user)
        db.session.commit()

        return {"message":"user registered"},201

@user.route('/users/<int:id>')
class User(MethodView):

    @user.response(200, UserSchema)
    def get(self, id):
        return UserModel.query.get_or_404(id)


@user.route('/login')
class Login(MethodView):

    @user.arguments(UserSchema)
    def post(self,loginData):
        user = UserModel.query.filter(
            UserModel.username == loginData['username']
        ).first()

        if user and user.password == loginData['password']:
            return {'token': create_access_token(identity=user.id)},200
        else:
            return abort(403)