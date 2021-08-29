#! /usr/bin/env python


import asyncio
import sys
from os import listdir


async def execute(service):
    while True:
        try:
            mod = __import__(f'daemons.{service}')
            module = getattr(mod, service)
            daemon = getattr(module, 'Daemon')
            await daemon().execute()
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(5)


async def main():
    if sys.argv[1] == "--all":
        services = list(
            map(
                lambda x: x[:-3],
                [file for file in listdir("daemons") if file.endswith(".py") and file != '__init__.py'],
            )
        )
    else:
        services = sys.argv[1:]
    await asyncio.gather(*[execute(service) for service in services])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
