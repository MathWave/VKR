from os import listdir

from SprintLib.testers.BaseTester import BaseTester, TestException


class JavaScriptTester(BaseTester):
    files = None

    def before_test(self):
        self.files = []
        for file in listdir(self.solution.testing_directory):
            if file.endswith(".js"):
                self.files.append(file)
        if not self.files:
            raise TestException("TE")

    @property
    def command(self):
        return f"node {' '.join(self.files)}"
