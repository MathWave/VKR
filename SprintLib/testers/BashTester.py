from os import listdir

from SprintLib.testers.BaseTester import BaseTester, TestException


class BashTester(BaseTester):
    file = None

    def before_test(self):
        for file in listdir(self.path):
            if file == 'solution.sh':
                self.call(f"chmod 777 {file}")
                self.file = file
                break
        if self.file is None:
            raise TestException("TE")

    @property
    def command(self):
        return f"./{self.file}"
