from helpers import Server, is_success
import os
import pytest

### Fixtures ###


@pytest.fixture(scope='function')
def server():
    """Return a server and clean it when the test is done"""
    s = Server("http://" + os.getenv("SERVER_URL"))
    yield s
    s.clean()

### Tests ###


def test_put_request_succeed(server):
    assert is_success(server.put("/hello/world", {"answer": 42}))


def test_put_request_twice_succeed(server):
    path = "/hello/world"
    data = {"answer": 42}
    server.put(path, data)
    assert is_success(server.put(path, data))


def test_get_request_succeed(server):
    path = "/hello/world"
    data = {"answer": 42}
    server.put(path, data)
    assert is_success(server.get(path))


def test_delete_request_succeed(server):
    path = "/hello/world"
    data = {"answer": 42}
    server.put(path, data)
    assert is_success(server.delete(path))


def test_get_request_content(server):
    path = "/hello/world"
    data = {"answer": 42}
    server.put(path, data)
    assert server.get(path).json() == data


def test_get_request_redirect_if_subpath(server):
    path = "/hello/world"
    sub_path = path + "/two"
    data = {"answer": 42}
    server.put(path, data)
    response = server.get(sub_path, allow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == path


def test_get_request_result_of_redirect_if_subpath(server):
    path = "/hello/world"
    sub_path = path + "/two"
    data = {"answer": 42}
    server.put(path, data)
    response = server.get(sub_path)
    assert is_success(response)
    assert response.json() == data
