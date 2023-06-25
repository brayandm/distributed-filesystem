from flask import Flask, Blueprint
import os

app = Flask(__name__)

apiv1 = Blueprint("v1", __name__, url_prefix="/v1")


@apiv1.route("/ping", methods=["GET"])
def hello_world():
    return "server " + os.environ.get("SERVER_ID") + " response: pong"


app.register_blueprint(apiv1)
