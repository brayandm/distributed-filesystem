import requests


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def upload_file(self, filepath):
        with open(filepath, "r") as f:
            content = f.read()

        filename = filepath.split("/")[-1]

        return self.store_file(filename, content)

    def store_file(self, filename, content):
        response = requests.post(
            self.host + ":" + str(self.port) + "/v1/store",
            json={"filename": filename, "content": content},
        )

        return response.text, response.status_code

    def get_file(self, filename):
        response = requests.get(
            self.host + ":" + str(self.port) + "/v1/get", json={"filename": filename}
        )

        return response.text, response.status_code

    def get_size(self, filename):
        response = requests.get(
            self.host + ":" + str(self.port) + "/v1/getsize",
            json={"filename": filename},
        )

        return response.text, response.status_code

    def delete_file(self, filename):
        response = requests.post(
            self.host + ":" + str(self.port) + "/v1/delete",
            json={"filename": filename},
        )

        return response.text, response.status_code
