from helpers import Server, server

# From those specifications:
# https://restfulapi.net/http-methods/
# https://hub.docker.com/r/jacopofar/demo-rest-server
# Delete will return 200 on success (not 202 nor 204)
# Put will return 200 on update (not 204)


def test_get_new_resource_returns_not_found(server):
    path = "/hello/world"
    response = server.get(path)
    assert response.status_code == 404


def test_get_existing_resource_returns_content(server):
    path = "/hello/world"
    data = {"answer": 42}
    server.put(path, data)
    response = server.get(path)
    assert response.status_code == 200
    assert response.json() == data


def test_get_child_resource_redirect_and_returns_content(server):
    parent_path = "/hello"
    child_path = parent_path + "/world"
    data = {"answer": 42}
    server.put(parent_path, data)
    response = server.get(child_path)
    assert response.status_code == 200
    assert response.json() == data
    # Check that we have been redirected once
    assert len(response.history) == 1
    previous_response = response.history[0]
    assert previous_response.status_code == 302
    assert previous_response.headers["Location"] == parent_path


def test_get_parent_resource_returns_not_found(server):
    parent_path = "/hello"
    child_path = parent_path + "/world"
    data = {"answer": 42}
    server.put(child_path, data)
    response = server.get(parent_path)
    assert response.status_code == 404


def test_put_new_resource_returns_created(server):
    path = "/hello/world"
    data = {"answer": 42}
    assert server.put(path, data).status_code == 201


# We assume that we only expect 200 as response code and
# not 204 which is also correct
def test_put_existing_resource_returns_ok_and_update(server):
    path = "/hello/world"
    data = {"answer": 42}
    new_data = {"answer": 1337}
    # Create a resource once
    server.put(path, data)
    # Update the resource
    assert server.put(path, new_data).status_code == 200
    assert server.get(path).json() == new_data


def test_put_child_resource_returns_ok_and_do_not_update_parent(server):
    parent_path = "/hello"
    child_path = parent_path + "/world"
    parent_data = {"answer": 42}
    child_data = {"answer": 1337}
    server.put(child_path, child_data)
    server.put(parent_path, parent_data)
    assert server.get(parent_path).json() == parent_data
    assert server.get(child_path).json() == child_data


def test_put_parent_resource_returns_ok_and_do_not_update_child(server):
    parent_path = "/hello"
    child_path = parent_path + "/world"
    parent_data = {"answer": 42}
    child_data = {"answer": 1337}
    server.put(parent_path, parent_data)
    server.put(child_path, child_data)
    assert server.get(parent_path).json() == parent_data
    assert server.get(child_path).json() == child_data


def test_delete_unknown_resource_returns_not_found(server):
    path = "/hello/world"
    assert server.delete(path).status_code == 404


# We assume that we only expect 200 as response code and
# not 202 nor 204 which are also correct
def test_delete_existing_resource_returns_ok_and_delete(server):
    path = "/hello/world"
    data = {"answer": 42}
    server.put(path, data)
    assert server.delete(path).status_code == 200
    # Make sure the resource is deleted
    assert server.get(path).status_code == 404


def test_delete_child_resource_returns_not_found_and_the_path_to_the_parent(server):
    parent_path = "/hello"
    expected_content = b"found a different key which is " + \
        bytes(parent_path[1:], encoding="utf-8") + b", not the exact one given"
    child_path = parent_path + "/world"
    parent_data = {"answer": 42}
    server.put(parent_path, parent_data)
    response = server.delete(child_path)
    assert response.status_code == 404
    assert response.content == expected_content
    assert server.get(parent_path).json() == parent_data


def test_delete_parent_resource_returns_not_found(server):
    parent_path = "/hello"
    child_path = parent_path + "/world"
    child_data = {"answer": 42}
    server.put(child_path, child_data)
    response = server.delete(parent_path)
    assert response.status_code == 404
