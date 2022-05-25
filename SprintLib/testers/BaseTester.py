from os import listdir, mkdir
from os.path import join, exists
from subprocess import call, TimeoutExpired
from tempfile import TemporaryDirectory

from Main.models.progress import Progress
from Sprint.settings import CONSTS
from SprintLib.queue import send_to_queue
from SprintLib.utils import Timer


class TestException(Exception):
    pass


class BaseTester:
    working_directory = "app"
    checker_code = None
    path = ""

    def before_test(self):
        files = [
            file
            for file in listdir(self.path)
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
        if code == 1:
            raise TestException("ML")
        elif code != 0:
            raise TestException("RE")
        result = (
            open(join(self.path, "output.txt"), "r")
            .read()
            .strip()
            .replace("\r\n", "\n")
        )
        print("got result", result)
        if self.checker_code is not None:
            print("using checker")
            with open(join(self.path, "expected.txt"), "w") as fs:
                fs.write(self.predicted)
            with open(join(self.path, "checker.py"), "w") as fs:
                fs.write(self.checker_code)
            code = call(
                f'docker exec -i solution_{self.solution.id}_checker sh -c "cd app && python checker.py"',
                shell=True,
                timeout=1,
            )
            if code != 0:
                raise TestException("WA")
        else:
            print("using simple check")
            if result != self.predicted:
                print("incorrect")
                raise TestException("WA")
            print("correct")

    def after_test(self):
        pass

    @property
    def command(self):
        return "./executable.exe"

    @property
    def build_command(self):
        return ""

    def call(self, command):
        print(f"Executing command: {command}")
        if exists(self.path):
            return call(f"cd {self.path} && {command}", shell=True)
        else:
            return call(command, shell=True)

    def __init__(self, solution):
        self.solution = solution

    def save_solution(self):
        self.solution.save()

    def _setup_networking(self):
        self.call(f"docker network create solution_network_{self.solution.id}")
        for file in self.solution.task.dockerfiles:
            add_name = file.filename[11:]
            with open(join(self.path, "Dockerfile"), "w") as fs:
                fs.write(file.text)
            self.call(f"docker build -t solution_image_{self.solution.id}_{add_name} .")
            run_command = (
                f"docker run "
                f"--hostname {add_name} "
                f"--network solution_network_{self.solution.id} "
                f"--name solution_container_{self.solution.id}_{add_name} "
                f"-t -d solution_image_{self.solution.id}_{add_name}"
            )
            print("run command", run_command)
            self.call(run_command)

    def notify(self):
        self.solution.user.userinfo.refresh_from_db()
        send_to_queue("notification", {
            "type": "solution",
            "solution_id": self.solution.id
        })

    def cleanup(self):
        self.save_solution()
        self.call(f"docker rm --force solution_{self.solution.id}")
        self.call(f"docker rm --force solution_{self.solution.id}_checker")
        for file in self.solution.task.dockerfiles:
            add_name = file.filename[11:]
            self.call(f"docker rm --force solution_container_{self.solution.id}_{add_name}")
            self.call(f"docker image rm solution_image_{self.solution.id}_{add_name}")
        self.call(f"docker network rm solution_network_{self.solution.id}")

    def save_progress(self):
        progress = Progress.objects.get(
            user=self.solution.user, task=self.solution.task
        )
        if progress.finished_time is None:
            progress.finished_time = self.solution.time_sent
            progress.finished = True
            progress.save()
            progress.increment_rating()

    def execute(self):
        self.solution.result = CONSTS["testing_status"]
        self.save_solution()
        with TemporaryDirectory(dir="/tmp") as self.path:
            for file in self.solution.solutionfiles:
                dirs = file.path.split("/")
                for i in range(len(dirs) - 1):
                    name = join(self.path, "/".join(dirs[: i + 1]))
                    if not exists(name):
                        mkdir(name)
                with open(join(self.path, file.path), "wb") as fs:
                    fs.write(file.bytes.replace(b"\r\n", b"\n"))
            for file in self.solution.task.extrafiles:
                with open(join(self.path, file.filename), "wb") as fs:
                    bts = file.bytes
                    fs.write(bts)
            print("Files copied")
            self._setup_networking()
            docker_command = f"docker run --network solution_network_{self.solution.id} --name solution_{self.solution.id} --memory=\"{self.solution.task.memory_limit}k\" --volume={self.path}:/{self.working_directory} -t -d {self.solution.language.image}"
            print(docker_command)
            call(docker_command, shell=True)
            checker = self.solution.task.checkerfile
            if checker is not None:
                self.checker_code = checker.text
                call(
                    f"docker run --network solution_network_{self.solution.id} --name solution_{self.solution.id}_checker --volume={self.path}:/app -t -d python:3.6",
                    shell=True,
                )
            print("Container created")
            try:
                self.before_test()
                print("before test finished")
                for test in self.solution.task.tests:
                    if not test.filename.endswith(".a"):
                        self.predicted = (
                            open(join(self.path, test.filename + ".a"), "r")
                            .read()
                            .strip()
                            .replace("\r\n", "\n")
                        )
                        print("predicted:", self.predicted)
                        self.solution.test = int(test.filename)
                        self.solution.extras[test.filename] = {
                            "predicted": self.predicted,
                            "output": "",
                        }
                        self.save_solution()
                        try:
                            self.test(test.filename)
                        finally:
                            if exists(join(self.path, "output.txt")):
                                try:
                                    self.solution.extras[test.filename][
                                        "output"
                                    ] = open(join(self.path, "output.txt"), "r").read()
                                except UnicodeDecodeError:
                                    self.solution.extras[test.filename]["output"] = ""
                            self.save_solution()
                self.after_test()
                self.solution.result = CONSTS["ok_status"]
                self.solution.test = None
                self.save_solution()
                self.save_progress()
            except TestException as e:
                self.solution.result = str(e)
            except TimeoutExpired:
                self.solution.result = "TL"
            except Exception as e:
                self.solution.result = "TE"
                print(e)
        self.save_solution()
        self.cleanup()
        self.notify()
