from os import listdir, mkdir
from os.path import join, exists
from subprocess import call, TimeoutExpired

from SprintLib.queue import notify
from Main.models import ExtraFile, SolutionFile
from Main.models.progress import Progress
from Sprint.settings import CONSTS
from SprintLib.utils import get_bytes, Timer


class TestException(Exception):
    pass


class BaseTester:
    working_directory = "app"
    checker_code = None

    def before_test(self):
        files = [
            file
            for file in listdir(self.solution.testing_directory)
            if file.endswith("." + self.solution.language.file_type)
        ]
        code = self.solution.exec_command(
            f'{self.build_command} {" ".join(files)}',
            working_directory=self.working_directory,
        )
        if code != 0:
            raise TestException("CE")

    def test(self, filename):
        with Timer(self.solution, filename):
            code = self.solution.exec_command(
                f"< {filename} {self.command} > output.txt",
                timeout=self.solution.task.time_limit / 1000,
            )
        if code != 0:
            raise TestException("RE")
        result = open(join(self.solution.testing_directory, "output.txt"), "r").read().strip().replace('\r\n', '\n')
        print("got result", result)
        if self.checker_code is not None:
            print('using checker')
            with open(join(self.path, 'expected.txt'), 'w') as fs:
                fs.write(self.predicted)
            with open(join(self.path, 'checker.py'), 'w') as fs:
                fs.write(self.checker_code)
            code = call(f'docker exec -i solution_{self.solution.id}_checker sh -c "cd app && python checker.py"', shell=True, timeout=1)
            if code != 0:
                raise TestException("WA")
        else:
            print('using simple check')
            if result != self.predicted:
                print('incorrect')
                raise TestException("WA")
            print('correct')

    def after_test(self):
        pass

    @property
    def command(self):
        return "./executable.exe"

    @property
    def build_command(self):
        return ""

    def call(self, command):
        return call(f'cd {self.path} && {command}', shell=True)

    @property
    def path(self):
        return join("solutions", str(self.solution.id))

    def __init__(self, solution):
        self.solution = solution

    def set_test(self, num):
        self.solution.result = CONSTS["testing_status"] + f"({num})"
        self.solution.save()

    def execute(self):
        if not exists("solutions"):
            mkdir("solutions")
        mkdir(self.path)
        for file in SolutionFile.objects.filter(solution=self.solution):
            dirs = file.path.split("/")
            for i in range(len(dirs) - 1):
                name = join(
                    self.path, "/".join(dirs[: i + 1])
                )
                if not exists(name):
                    mkdir(name)
            with open(
                join(self.path, file.path), "wb"
            ) as fs:
                fs.write(get_bytes(file.fs_id).replace(b"\r\n", b"\n"))
        dockerfiles = sorted(list(ExtraFile.objects.filter(filename__startswith="Dockerfile", readable=True, task=self.solution.task)), key=lambda x: x.filename)
        self.call(f"docker network create solution_network_{self.solution.id}")
        for file in dockerfiles:
            with open(join(self.path, 'Dockerfile'), 'w') as fs:
                fs.write(file.text)
            self.call(f"docker build -t solution_image_{self.solution.id}_{file.filename} .".lower())
            self.call(f"docker run --network solution_network_{self.solution.id} --name solution_container_{self.solution.id}_{file.filename} -t -d solution_image_{self.solution.id}_{file.filename}".lower())
        self.solution.result = CONSTS["testing_status"]
        self.solution.save()
        docker_command = f"docker run --network solution_network_{self.solution.id} --name solution_{self.solution.id} --volume=/sprint-data/solutions/{self.solution.id}:/{self.working_directory} -t -d {self.solution.language.image}"
        print(docker_command)
        call(docker_command, shell=True)
        checker = ExtraFile.objects.filter(task=self.solution.task, filename='checker.py').first()
        if checker is not None:
            self.checker_code = checker.text
            call(f"docker run --name solution_{self.solution.id}_checker --volume=/sprint-data/solutions/{self.solution.id}:/app -t -d python:3.6", shell=True)
        print("Container created")
        for file in ExtraFile.objects.filter(task=self.solution.task):
            with open(
                join(self.path, file.filename), 'wb'
            ) as fs:
                bts = get_bytes(file.fs_id)
                fs.write(bts)
        print("Files copied")
        try:
            self.before_test()
            print("before test finished")
            for test in self.solution.task.tests:
                if not test.filename.endswith(".a"):
                    self.predicted = ExtraFile.objects.get(
                        task=self.solution.task, filename=test.filename + ".a"
                    ).text.strip().replace('\r\n', '\n')
                    print('predicted:', self.predicted)
                    self.solution.test = int(test.filename)
                    self.solution.extras[test.filename] = {'predicted': self.predicted, 'output': ''}
                    self.solution.save()
                    try:
                        self.test(test.filename)
                    finally:
                        if exists(join(self.path, "output.txt")):
                            try:
                                self.solution.extras[test.filename]['output'] = open(join(self.path, 'output.txt'), 'r').read()
                            except UnicodeDecodeError:
                                self.solution.extras[test.filename]['output'] = ''
            self.after_test()
            self.solution.result = CONSTS["ok_status"]
            self.solution.test = None
            progress = Progress.objects.get(
                user=self.solution.user, task=self.solution.task
            )
            if progress.finished_time is None:
                progress.finished_time = self.solution.time_sent
                progress.finished = True
                progress.save()
                progress.increment_rating()
        except TestException as e:
            self.solution.result = str(e)
        except TimeoutExpired:
            self.solution.result = "TL"
        except Exception as e:
            self.solution.result = "TE"
            raise e
        self.solution.save()
        call(f"docker rm --force solution_{self.solution.id}", shell=True)
        call(f"docker rm --force  solution_{self.solution.id}_checker", shell=True)
        self.solution.user.userinfo.refresh_from_db()
        notify(
            self.solution.user,
            "solution_result",
            f"Задача: {self.solution.task.name}\n"
            f"Результат: {self.solution.result}\n"
            f"Очки решения: {Progress.by_solution(self.solution).score}\n"
            f"Текущий рейтинг: {self.solution.user.userinfo.rating}")
