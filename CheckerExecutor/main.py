from multiprocessing import Process
from os import getenv, environ
from os.path import join
from tempfile import TemporaryDirectory
from time import sleep
from zipfile import ZipFile

from requests import get

from language import languages
from testers import *

host = "http://dev.sprinthub.ru/"


def process_solution(path, data, language_id, solution_id, timeout):
    with open(join(path, "package.zip"), 'wb') as fs:
        fs.write(data)
    with ZipFile(join(path, "package.zip"), 'r') as zip_ref:
        zip_ref.extractall(path)
    language = languages[language_id]
    try:
        result = eval(language.work_name + "Tester")(path, solution_id, language_id, timeout).execute()
    except Exception as e:
        print(str(e))
        result = "TE"
    return result


def poll(token):
    correct_token = True
    while correct_token:
        code = get(f"{host}checker/status", params={"token": token}).status_code
        if code != 200:
            correct_token = False
        else:
            sleep(2)


def main():
    request = get(f"{host}checker/get_dynamic", params={"token": getenv("TOKEN")})
    if request.status_code != 200:
        print("Error happened: " + request.json()['status'])
        exit(1)
    dynamic_token = request.json()['token']
    p = Process(target=poll, args=(dynamic_token,))
    p.start()
    while True:
        data = get(f"{host}checker/available", params={"token": dynamic_token})
        if data.status_code == 200:
            sleep(2)
            continue
        elif data.status_code == 201:
            with TemporaryDirectory() as tempdir:
                result = process_solution(
                    tempdir,
                    data.content,
                    int(data.headers['language_id']),
                    int(data.headers['solution_id']),
                    int(data.headers['timeout']),
                )
                get(f"{host}checker/set_result", params={
                    "token": dynamic_token,
                    "solution_id": data.headers['solution_id'],
                    "result": result
                })
        elif data.status_code == 403:
            print("token removed")
            exit(1)
        else:
            print("unknown status")
            exit(1)


if __name__ == '__main__':
    main()
