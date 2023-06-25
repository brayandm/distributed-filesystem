from flask import Flask, Blueprint, request
import os

app = Flask(__name__)

apiv1 = Blueprint("v1", __name__, url_prefix="/v1")


@apiv1.route("/ping", methods=["GET"])
def hello_world():
    return "server " + os.environ.get("SERVER_ID") + " response: pong"


@apiv1.route("/store", methods=["POST"])
def store_file():
    if (
        not request.json
        or not "filename" in request.json
        or not "content" in request.json
    ):
        return "filename or content not provided", 400

    filename = request.json["filename"]
    content = request.json["content"]

    storage_path = "storage/server" + os.environ.get("SERVER_ID")

    if os.path.exists(storage_path + "/" + filename):
        return "file already exists", 400

    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    with open(storage_path + "/" + filename, "w") as f:
        f.write(content)

    return "file stored", 200


@apiv1.route("/delete", methods=["POST"])
def delete_file():
    if not request.json or not "filename" in request.json:
        return "filename not provided", 400

    filename = request.json["filename"]

    storage_path = "storage/server" + os.environ.get("SERVER_ID")

    if not os.path.exists(storage_path + "/" + filename):
        return "file does not exist", 400

    os.remove(storage_path + "/" + filename)

    return "file deleted", 200


app.register_blueprint(apiv1)
