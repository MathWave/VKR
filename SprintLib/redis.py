import os

import redis


def get_redis():
    return redis.Redis(host=os.getenv("REDIS_HOST", "127.0.0.1"))


def get(key):
    with get_redis() as r:
        return r.get(key)


def set(key, value):
    with get_redis() as r:
        return r.set(key, value)


def lock(name='lock'):
    def dec(fun):
        def wrapper(*args, **kwargs):
            with get_redis() as r:
                with r.lock(name):
                    return fun(*args, **kwargs)

        return wrapper
    return dec
