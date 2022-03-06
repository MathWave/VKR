import os
from os import mkdir
from os.path import exists

from aiohttp import web
from FileStorage.routes import setup_routes


def runserver():
    app = web.Application()
    setup_routes(app)
    if not exists("data"):
        mkdir("data")
    if not exists("data/meta.txt"):
        with open("data/meta.txt", "w") as fs:
            fs.write("0")
    web.run_app(app, host="0.0.0.0", port=5555)


if __name__ == "__main__":
    runserver()
