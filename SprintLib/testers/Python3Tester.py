from os import listdir

from SprintLib.testers.BaseTester import BaseTester, TestException


class Python3Tester(BaseTester):
    file = None

    def before_test(self):
        no_files = [file.filename for file in self.solution.task.files]
        for file in listdir(self.solution.testing_directory):
            if file.endswith(".py") and file not in no_files:
                self.file = file
                break
        if self.file is None:
            raise TestException("TE")

    @property
    def command(self):
        return f"python3 {self.file}"
