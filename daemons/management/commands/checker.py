from os import getenv, remove, listdir, walk
from os.path import join, isfile
from tempfile import TemporaryDirectory
from threading import Thread
from time import sleep
from zipfile import ZipFile

from django.core.management import BaseCommand
from requests import get

from Main.models import Solution, Task, ExtraFile, SolutionFile
from SprintLib.language import languages
from SprintLib.testers import *


host = 'http://192.168.0.146:8000/'


class Command(BaseCommand):
    help = "Tests solution"

    def poll(self, token):
        correct_token = True
        while correct_token:
            code = get(f"{host}checker/status", params={"token": token}).status_code
            if code != 200:
                correct_token = False
            else:
                sleep(2)

    def handle(self, *args, **options):
        print("Starting checker")
        request = get(f"{host}checker/get_dynamic", params={"token": getenv("TOKEN")})
        if request.status_code != 200:
            print("Error happened: " + request.json()['status'])
            exit(1)
        print("Got dynamic token")
        dynamic_token = request.json()['token']
        p = Thread(target=self.poll, args=(dynamic_token,))
        p.start()
        while True:
            data = get(f"{host}checker/available", params={"token": dynamic_token})
            if data.status_code == 200:
                sleep(2)
                continue
            elif data.status_code == 201:
                solution = self.create_solution(data)
                print("handled solution", solution.id)
                tester_class = eval(solution.language.work_name + "Tester")

                class LocalTester(DistantTester, tester_class):
                    ...

                tester = LocalTester(solution)
                tester.host = host
                tester.token = dynamic_token
                try:
                    tester.execute()
                except Exception as e:
                    print(e)
                    solution.result = "TE"
                tester.save_solution()
            elif data.status_code == 403:
                print("token removed")
                exit(1)
            else:
                print("unknown status")
                exit(1)

    def create_solution(self, data):
        with TemporaryDirectory(dir='/tmp') as path:
            with open(join(path, "package.zip"), 'wb') as fs:
                fs.write(data.content)
            with ZipFile(join(path, "package.zip"), 'r') as zip_ref:
                zip_ref.extractall(path)
            remove(join(path, "package.zip"))

            solution = Solution(
                id=int(data.headers['solution_id']),
                language_id=int(data.headers['language_id']),
                task=Task(
                    time_limit=int(data.headers['timeout']),
                )
            )

            solution.task.extrafiles = [ExtraFile(
                filename=file,
                task=solution.task
            ) for file in listdir(path) if isfile(join(path, file))]
            for file in solution.task.extrafiles:
                file.bytes = open(join(path, file.filename), 'rb').read()
            solution.solutionfiles = [
                SolutionFile(
                    path=join(directory, file)[len(join(path, 'solution')) + 1:],
                    solution=solution,
                )
                for directory, _, files in walk(join(path, 'solution')) for file in files
            ]
            for file in solution.solutionfiles:
                file.bytes = open(join(path, 'solution', file.path), 'rb').read()

        return solution
