import requests
import os
import pytest


@pytest.fixture(scope='function')
def server():
    """Return a server and clean it when the test is done"""
    s = Server(os.getenv("SERVER_URL"))
    yield s
    s.clean()


class Server:
    def __init__(self, base_uri):
        self.base_uri = base_uri
        self._data = {}

    def put(self, path: str, data):
        """Perform a put request to the server and return the response"""
        response = requests.put(self.base_uri + path, json=data)
        if response:
            self._data[path] = data
        return response

    def get(self, path, **kwargs):
        """Perform a get request to the server and return the response"""
        return requests.get(self.base_uri + path, **kwargs)

    def delete(self, path, **kwargs):
        """Perform a delete request to the server and return the response"""
        response = requests.delete(self.base_uri + path, **kwargs)
        try:
            del self._data[path]
        except KeyError:
            pass
        return response

    def clean(self):
        for path in self._data.keys():
            requests.delete(self.base_uri + path)
        self._data = {}
