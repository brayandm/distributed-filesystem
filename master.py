from flask import Flask, Blueprint, request, jsonify
import os
from redis import Redis
import uuid
import requests

redis = Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"))

app = Flask(__name__)

apiv1 = Blueprint("v1", __name__, url_prefix="/v1")

storage_servers = [
    "http://storageserver1.test",
    "http://storageserver2.test",
    "http://storageserver3.test",
]


@apiv1.route("/getsize", methods=["GET"])
def get_size():
    if not request.json or not "filename" in request.json:
        return "filename not provided", 400

    filename = request.json["filename"]

    if not redis.exists(filename):
        return "file does not exist", 400

    chunk_servers = redis.lrange(filename, 0, -1)

    size = 0

    for chunk_server in chunk_servers:
        chunk_filename, chunk_server = chunk_server.decode("utf-8").split("@")

        response = requests.get(
            chunk_server + "/v1/getsize", json={"filename": chunk_filename}
        )

        size += int(response.text)

    return str(size), 200


def get_server():
    server_id = int(redis.incr("server_counter")) - 1

    return storage_servers[server_id % len(storage_servers)]


@apiv1.route("/ping", methods=["GET"])
def hello_world():
    return "master response: pong"


@apiv1.route("/get", methods=["GET"])
def get_file():
    if not request.json or not "filename" in request.json:
        return "filename not provided", 400

    filename = request.json["filename"]

    if not redis.exists(filename):
        return "file does not exist", 400

    chunk_servers = redis.lrange(filename, 0, -1)

    content = ""

    for chunk_server in chunk_servers:
        chunk_filename, chunk_server = chunk_server.decode("utf-8").split("@")

        response = requests.get(
            chunk_server + "/v1/get", json={"filename": chunk_filename}
        )

        content += response.text

    return content, 200


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

    if redis.exists(filename):
        return "file already exists", 400

    chunk_size = int(os.environ.get("CHUNK_SIZE"))

    chunks = [content[i : i + chunk_size] for i in range(0, len(content), chunk_size)]

    chunk_servers = []

    for i in range(len(chunks)):
        storage_server = get_server()

        chunk_filename = str(uuid.uuid4())

        chunk_servers.append(chunk_filename + "@" + storage_server)

        requests.post(
            storage_server + "/v1/store",
            json={"filename": chunk_filename, "content": chunks[i]},
        )

    redis.rpush(filename, *chunk_servers)

    return "file stored", 200


@apiv1.route("/delete", methods=["POST"])
def delete_file():
    if not request.json or not "filename" in request.json:
        return "filename not provided", 400

    filename = request.json["filename"]

    if not redis.exists(filename):
        return "file does not exist", 400

    chunk_servers = redis.lrange(filename, 0, -1)

    for chunk_server in chunk_servers:
        chunk_filename, chunk_server = chunk_server.decode("utf-8").split("@")

        requests.post(chunk_server + "/v1/delete", json={"filename": chunk_filename})

    redis.delete(filename)

    return "file deleted", 200


app.register_blueprint(apiv1)
