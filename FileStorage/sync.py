import threading

import aiofiles


def synchronized_method(method):
    outer_lock = threading.Lock()
    lock_name = "__" + method.__name__ + "_lock" + "__"

    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name):
                setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)
    return sync_method


@synchronized_method
async def write_meta(request):
    async with aiofiles.open("data/meta.txt", "r") as fs:
        num = int(await fs.read()) + 1
    async with aiofiles.open("data/meta.txt", "w") as fs:
        await fs.write(str(num))
    return num
