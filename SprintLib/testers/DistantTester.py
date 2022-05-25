import json

from requests import get

from SprintLib.testers import BaseTester


class DistantTester(BaseTester):
    host = ""
    token = ""

    def request(self, method, params=None):
        if params is None:
            params = {}
        return get(f'{self.host}checker/{method}', params={**{
            "token": self.token,
            "solution_id": self.solution.id,
        }, **params})

    def save_solution(self):
        self.request("save_solution", {
            "test": self.solution.test,
            "result": self.solution.result,
            "extras": json.dumps(self.solution.extras)
        })

    def notify(self):
        self.request("notify")

    def save_progress(self):
        self.request("save_progress")
