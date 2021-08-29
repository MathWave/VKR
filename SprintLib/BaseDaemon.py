import asyncio
import sys
from time import sleep


class BaseDaemon:
    def command(self):
        raise NotImplementedError()

    async def execute(self):
        cmd = self.command()
        proc = await asyncio.create_subprocess_shell(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        stdout, stderr = await proc.communicate()
        print(f"[{cmd!r} exited with {proc.returncode}]")
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")
