from SprintLib.testers.BaseTester import BaseTester


class CppTester(BaseTester):
    @property
    def build_command(self):
        return "g++ -o executable.exe"
