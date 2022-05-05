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

    def cleanup(self):
        self.save_solution()
        self.call(f"docker rm --force solution_{self.solution.id}")
        self.call(f"docker rm --force solution_{self.solution.id}_checker")
        for file in self.solution.task.dockerfiles:
            add_name = file.filename[11:]
            self.call(f"docker rm --force solution_container_{self.solution.id}_{add_name}")
            self.call(f"docker image rm solution_image_{self.solution.id}_{add_name}")
        self.call(f"docker network rm solution_network_{self.solution.id}")

    def save_progress(self):
        self.request("save_progress")
