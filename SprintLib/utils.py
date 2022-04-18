import datetime
from random import choice

from requests import get, post

from Sprint import settings


def write_bytes(data: bytes):
    url = settings.FS_HOST + ":" + str(settings.FS_PORT) + "/upload_file"
    print(url)
    try:
        return post(url, data=data).json()["id"]
    except Exception:
        return 0


def get_bytes(num: int) -> bytes:
    url = settings.FS_HOST + ":" + str(settings.FS_PORT) + "/get_file?id=" + str(num)
    print(url)
    try:
        return get(url).content
    except Exception:
        return b''


def delete_file(num: int):
    url = settings.FS_HOST + ":" + str(settings.FS_PORT) + "/delete_file?id=" + str(num)
    print(url)
    try:
        post(url)
    except Exception:
        ...


def generate_token():
    letters = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    return ''.join([choice(letters) for _ in range(30)])


class Timer:
    start_time = None
    end_time = None

    def __init__(self, solution, test):
        self.solution = solution
        self.test = test

    def __enter__(self):
        assert self.start_time is None
        self.start_time = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.datetime.now()
        self.solution.extras[self.test]['time_spent'] = (self.end_time - self.start_time).total_seconds() * 1000
