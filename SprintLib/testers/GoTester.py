from SprintLib.testers.BaseTester import BaseTester


class GoTester(BaseTester):
    working_directory = "../app"

    def build_command(self):
        return "go build -o executable.exe"
