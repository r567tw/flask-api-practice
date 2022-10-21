from flask import Flask
from flask_smorest import Api
from resources.store import store
from resources.item import item

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = "/uploads"
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


@app.get('/')
def HelloWorld():
    return "HelloWorld from dockerfile"


@app.route("/upload", methods=["post"])
def upload():
    image = request.files['image']
    image.save("./{}".format(image.filename))
    return {"message": "image upload"}, 201


api = Api(app)

api.register_blueprint(item)
api.register_blueprint(store)
