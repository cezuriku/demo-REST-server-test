#!/usr/bin/env python3
import os
import requests


def main():
    base_uri = "http://" + os.getenv("SERVER_URL")
    print(requests.put(base_uri + "/hello", json={"answer": 42}))
    print(requests.get(base_uri + "/hello").content)


if __name__ == "__main__":
    main()
