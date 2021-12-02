from os import listdir

from SprintLib.testers.BaseTester import BaseTester, TestException


class JavaTester(BaseTester):
    _executable = None

    def before_test(self):
        files = [
            file
            for file in listdir(self.solution.testing_directory)
            if file.endswith(".java")
        ]
        code = self.solution.exec_command(f"javac {' '.join(files)}")
        if code != 0:
            raise TestException("CE")
        for file in listdir(self.solution.testing_directory):
            if file.endswith(".class"):
                self._executable = file.rstrip(".class")
                break
        if self._executable is None:
            raise TestException("TE")

    @property
    def command(self):
        return f"java -classpath . {self._executable}"
