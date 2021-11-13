from os import listdir, mkdir
from os.path import join, exists
from subprocess import call, TimeoutExpired

from Main.management.commands.bot import bot
from Main.models import ExtraFile, SolutionFile
from Main.models.progress import Progress
from Sprint.settings import CONSTS
from SprintLib.utils import get_bytes


class TestException(Exception):
    pass


class BaseTester:
    working_directory = "app"

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
        code = self.solution.exec_command(
            f"< {filename} {self.command} > output.txt",
            timeout=self.solution.task.time_limit / 1000,
        )
        if code != 0:
            raise TestException("RE")
        result = open(join(self.solution.testing_directory, "output.txt"), "r").read()
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
        if not exists("solutions"):
            mkdir("solutions")
        mkdir("solutions/" + str(self.solution.id))
        for file in SolutionFile.objects.filter(solution=self.solution):
            dirs = file.path.split('/')
            for i in range(len(dirs) - 1):
                name = join(str("solutions/" + self.solution.id), '/'.join(dirs[:i + 1]))
                if not exists(name):
                    mkdir(name)
            with open(join("solutions/" + str(self.solution.id), file.path), 'wb') as fs:
                fs.write(get_bytes(file.fs_id))
        self.solution.result = CONSTS["testing_status"]
        self.solution.save()
        docker_command = f"docker run --name solution_{self.solution.id} --volume=/sprint-data/solutions/{self.solution.id}:/{self.working_directory} -t -d {self.solution.language.image}"
        print(docker_command)
        call(docker_command, shell=True)
        print("Container created")
        for file in ExtraFile.objects.filter(task=self.solution.task):
            with open(join("solutions/" + str(self.solution.id), file.filename), 'wb') as fs:
                fs.write(get_bytes(file.fs_id))
        print("Files copied")
        try:
            self.before_test()
            print("before test finished")
            for test in self.solution.task.tests:
                if not test.filename.endswith(".a"):
                    self.predicted = ExtraFile.objects.get(
                        task=self.solution.task, filename=test.filename + ".a"
                    ).text
                    self.test(test.filename)
            self.after_test()
            self.solution.result = CONSTS["ok_status"]
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
            print(str(e))
        self.solution.save()
        call(f"docker rm --force solution_{self.solution.id}", shell=True)
        self.solution.user.userinfo.refresh_from_db()
        if self.solution.user.userinfo.notification_solution_result:
            bot.send_message(
                self.solution.user.userinfo.telegram_chat_id,
                f"Задача: {self.solution.task.name}\n"
                f"Результат: {self.solution.result}\n"
                f"Очки решения: {Progress.by_solution(self.solution).score}\n"
                f"Текущий рейтинг: {self.solution.user.userinfo.rating}",
                parse_mode="html",
            )
