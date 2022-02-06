from requests import get, post

from Sprint import settings


def write_bytes(data: bytes):
    url = settings.FS_HOST + ":" + str(settings.FS_PORT) + "/upload_file"
    print(url)
    return post(url, data=data).json()["id"]


def get_bytes(num: int) -> bytes:
    url = settings.FS_HOST + ":" + str(settings.FS_PORT) + "/get_file?id=" + str(num)
    print(url)
    return get(url).content


def delete_file(num: int):
    url = settings.FS_HOST + ":" + str(settings.FS_PORT) + "/delete_file?id=" + str(num)
    print(url)
    post(url)
