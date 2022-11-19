import os
from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv
from resources.store import store
from resources.item import item
from resources.user import user
from db import db
from flask_jwt_extended import JWTManager
import models
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    # app.config['UPLOAD_FOLDER'] = "/uploads"
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app,db)

    # @app.before_first_request
    # def create_table():
    #     db.create_all()

    @app.get('/')
    def HelloWorld():
        return "HelloWorld from dockerfile"

    @app.route("/upload", methods=["post"])
    def upload():
        image = request.files['image']
        image.save("./{}".format(image.filename))
        return {"message": "image upload"}, 201

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claim(identity):
        if identity == 1:
            return {"is_admin": 1}
        else:
            return {"is_admin": 0}


    @jwt.invalid_token_loader
    def invalid_token(error):
        return {"message": "invalid token"},403

    api.register_blueprint(item)
    api.register_blueprint(store)
    api.register_blueprint(user)

    return app
