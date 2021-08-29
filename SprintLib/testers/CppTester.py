from os import listdir

from SprintLib.testers import BaseTester, TestException


class CppTester(BaseTester):
    @property
    def build_command(self):
        return "g++ -o executable.exe"
