from SprintLib.testers.BaseTester import BaseTester


class CSharpTester(BaseTester):
    @property
    def build_command(self):
        return "csc /out:executable.exe"

    @property
    def command(self):
        return "mono executable.exe"
