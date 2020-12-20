from helpers import Server
import os


# Not in the specifications
def test_put_request_returns_201():
    server = Server("http://" + os.getenv("SERVER_URL"))
    path = "/hello/world"
    data = {"answer": 42}
    assert server.put(path, data).status_code == 201
