from os import listdir

from SprintLib.testers.BaseTester import BaseTester, TestException


class Python3Tester(BaseTester):
    file = None

    def before_test(self):
        for file in listdir(self.path):
            if file == 'solution.py':
                self.file = file
                break
        if self.file is None:
            raise TestException("TE")

    @property
    def command(self):
        return f"python3 {self.file}"
