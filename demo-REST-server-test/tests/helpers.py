import requests


class Server:
    def __init__(self, base_uri):
        self.base_uri = base_uri

    def put(self, path, data):
        """Perform a put request to the server and return the result"""
        return requests.put(self.base_uri + path, json=data)

    def get(self, path):
        """Perform a get request to the server and return the result"""
        return requests.get(self.base_uri + path)

    def delete(self, path):
        """Perform a delete request to the server and return the result"""
        return requests.delete(self.base_uri + path)
