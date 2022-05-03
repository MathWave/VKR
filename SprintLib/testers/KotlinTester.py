from os import listdir

from SprintLib.testers.BaseTester import BaseTester, TestException


class KotlinTester(BaseTester):
    def before_test(self):
        files = [
            file
            for file in listdir(self.path)
            if file.endswith(".kt")
        ]
        code = self.solution.exec_command(
            f'kotlinc {" ".join(files)} -include-runtime -d solution.jar'
        )
        if code != 0:
            raise TestException("CE")

    @property
    def command(self):
        return "java -jar solution.jar"
