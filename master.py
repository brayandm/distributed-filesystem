from flask import Flask, Blueprint
import os
from redis import Redis

redis = Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"))

app = Flask(__name__)

apiv1 = Blueprint("v1", __name__, url_prefix="/v1")


@apiv1.route("/ping", methods=["GET"])
def hello_world():
    return "master response: pong"


app.register_blueprint(apiv1)
