from os import listdir

from SprintLib.testers.BaseTester import BaseTester, TestException


class SwiftTester(BaseTester):
    def before_test(self):
        files = [
            file
            for file in listdir(self.path)
            if file.endswith(".swift")
        ]
        code = self.solution.exec_command(
            f'swiftc {" ".join(files)} -o solution'
        )
        if code != 0:
            raise TestException("CE")

    @property
    def command(self):
        return "./solution"
