from helpers import Server, server
import pytest
import json

# From those specifications:
# https://hub.docker.com/r/jacopofar/demo-rest-server
# The URI path can be up to 100 characters
# The data can be up to 500KB
# Max safe integer is 9007199254740991 (due to js restrictions)
# The URI Path can only contain integers, lowercase, uppercase,
#     hyphen(not at the beginning nor the end)
# RFC 3986 defines URIs as case-sensitive except for the scheme and host components.


def test_accept_path_of_100_chars_and_50_levels(server):
    path = "/a" * 50
    data = {"answer": 42}
    assert server.put(path, data).status_code == 201
    response = server.get(path, allow_redirects=False)
    assert response.status_code == 200
    assert response.json() == data


def test_accept_path_of_100_chars(server):
    path = "/" + "a" * 99
    data = {"answer": 42}
    assert server.put(path, data).status_code == 201
    response = server.get(path, allow_redirects=False)
    assert response.status_code == 200
    assert response.json() == data


def test_accept_complex_path(server):
    path = "/lowercase123456-UPPERCASE"
    data = {"answer": 42}
    assert server.put(path, data).status_code == 201
    response = server.get(path, allow_redirects=False)
    assert response.status_code == 200
    assert response.json() == data


def test_path_is_case_sensitive(server):
    path_lowercase = "/path"
    data_lowercase = "lowercase data"
    path_uppercase = "/PATH"
    data_uppercase = "UPPERCASE DATA"
    assert server.put(path_lowercase, data_lowercase).status_code == 201
    assert server.put(path_uppercase, data_uppercase).status_code == 201
    assert server.get(path_lowercase).json() == data_lowercase
    assert server.get(path_uppercase).json() == data_uppercase


@pytest.mark.parametrize(
    "data",
    [
        "Hello world!",
        u"こんにちは世界 😀",  # Unicode string
        9007199254740991,  # Number integer
        123e-5,  # Number decimal
        {"key": "value"},  # dict(python) object(JS)
        [0, 1, 2, 3, 4],
        True
    ])
def test_handle_several_data_types(server, data):
    path = "/data"
    assert server.put(path, data).status_code == 201
    response = server.get(path, allow_redirects=False)
    assert response.status_code == 200
    assert response.json() == data


def test_store_big_data(server):
    path = "/big-data"
    # Open a file of more than 500kB
    with open("big_data.json") as file:
        data = json.load(file)
        assert len(json.dumps(data)) > 500000
        assert server.put(path, data).status_code == 201
        response = server.get(path, allow_redirects=False)
        assert response.status_code == 200
        assert response.json() == data
