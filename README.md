demo-REST-server-test
===================

The purpose of this repository is to test the demo-REST-server:
https://hub.docker.com/r/jacopofar/demo-rest-server

## To run the tests ##

    docker-compose run --rm test
    # To clean after since the server will still be up as it is a dependency of the test docker
    docker-compose down

## To rebuild the image once you have made changes ##

    docker-compose build test
