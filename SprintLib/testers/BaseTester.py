from os import listdir
from os.path import join
from shutil import copyfile, rmtree
from subprocess import call, TimeoutExpired

from Main.models import ExtraFile
from Sprint.settings import CONSTS
from SprintLib.utils import copy_content


class TestException(Exception):
    pass


class BaseTester:
    working_directory = "app"

    def before_test(self):
        files = [file for file in listdir(self.solution.testing_directory) if file.endswith('.' + self.solution.language.file_type)]
        code = self.solution.exec_command(f'{self.build_command} {" ".join(files)}', working_directory=self.working_directory)
        if code != 0:
            raise TestException('CE')

    def test(self, filename):
        code = self.solution.exec_command(
            f"< {filename} {self.command} > output.txt",
            timeout=self.solution.task.time_limit / 1000,
        )
        if code != 0:
            raise TestException("RE")
        result = open(
            join(self.solution.testing_directory, "output.txt"), "r"
        ).read()
        if result.strip() != self.predicted.strip():
            raise TestException("WA")

    def after_test(self):
        pass

    @property
    def command(self):
        return "./executable.exe"

    @property
    def build_command(self):
        return ""

    def __init__(self, solution):
        self.solution = solution

    def execute(self):
        copy_content(self.solution.directory, self.solution.testing_directory, ('test_dir',))
        self.solution.result = CONSTS["testing_status"]
        self.solution.save()
        call(
            f"docker run --name solution_{self.solution.id} --volume={self.solution.testing_directory}:/{self.working_directory} -t -d {self.solution.language.image}",
            shell=True,
        )
        for file in ExtraFile.objects.filter(task=self.solution.task):
            copyfile(file.path, join(self.solution.testing_directory, file.filename))
        try:
            self.before_test()
            for test in self.solution.task.tests:
                if not test.filename.endswith(".a"):
                    self.predicted = ExtraFile.objects.get(
                        task=self.solution.task, filename=test.filename + ".a"
                    ).text
                    self.test(test.filename)
            self.after_test()
            self.solution.result = CONSTS["ok_status"]
        except TestException as e:
            self.solution.result = str(e)
        except TimeoutExpired:
            self.solution.result = "TL"
        except Exception as e:
            self.solution.result = "TE"
            print(str(e))
        self.solution.save()
        call(f"docker rm --force solution_{self.solution.id}", shell=True)
        rmtree(self.solution.testing_directory)
