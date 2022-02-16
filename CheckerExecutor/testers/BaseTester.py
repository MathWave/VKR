from os import listdir
from os.path import join, exists
from subprocess import call, TimeoutExpired

from language import *


class TestException(Exception):
    pass


class BaseTester:
    working_directory = "app"
    checker_code = None

    def exec_command(self, command, working_directory="app", timeout=None):
        return call(
            f'docker exec -i solution sh -c "cd {working_directory} && {command}"',
            shell=True,
            timeout=timeout,
        )

    def before_test(self):
        files = [
            file
            for file in listdir(self.path)
            if file.endswith("." + self.language.file_type)
        ]
        code = self.exec_command(
            f'{self.build_command} {" ".join(files)}',
            working_directory=self.working_directory,
        )
        if code != 0:
            raise TestException("CE")

    def test(self, filename):
        code = self.exec_command(
            f"< {filename} {self.command} > output.txt",
            timeout=self.timeout / 1000,
        )
        if code != 0:
            raise TestException("RE")
        result = open(join(self.path, "output.txt"), "r").read().strip().replace('\r\n', '\n')
        print("got result", result)
        if self.checker_code is not None:
            print('using checker')
            with open(join(self.path, 'expected.txt'), 'w') as fs:
                fs.write(self.predicted)
            with open(join(self.path, 'checker.py'), 'w') as fs:
                fs.write(self.checker_code)
            code = call(f'docker exec -i checker sh -c "cd app && python checker.py"', shell=True, timeout=1)
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

    @property
    def path(self):
        return self._path

    @property
    def language(self):
        return languages[self.language_id]

    def __init__(self, path, solution_id, language_id, timeout):
        self.solution_id = solution_id
        self._path = path
        self.language_id = language_id
        self.timeout = timeout

    def execute(self):
        docker_command = f"docker run --name solution --volume={self.path}:/{self.working_directory} -t -d {self.language.image}"
        print(docker_command)
        call(docker_command, shell=True)
        checker = join(self.path, 'checker.py')
        if exists(checker):
            self.checker_code = open(checker, 'r').read()
            call(f"docker run --name checker --volume={self.path}:/app -t -d python:3.6", shell=True)
        print("Container created")
        result = None
        try:
            self.before_test()
            print("before test finished")
            for file in listdir(self.path):
                if not file.endswith(".a") and exists(join(self.path, file + '.a')):
                    self.predicted = open(join(self.path, file + '.a'), 'r').read().strip().replace('\r\n', '\n')
                    print('predicted:', self.predicted)
                    self.test(file)
            self.after_test()
            result = "OK"
        except TestException as e:
            result = str(e)
        except TimeoutExpired:
            result = "TL"
        except Exception as e:
            print(str(e))
            result = "TE"
        call(f"docker rm --force solution", shell=True)
        call(f"docker rm --force checker", shell=True)
        return result
