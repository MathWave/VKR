import json
from enum import Enum, auto
from typing import Union

import pika

from Sprint import settings


def send_testing(solution):
    if solution.set is not None and len(solution.set.checkers.all()) != 0:
        return
    with pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBIT_HOST, port=settings.RABBIT_PORT)
    ) as connection:
        channel = connection.channel()
        channel.queue_declare(queue="test")
        channel.basic_publish(
            exchange="",
            routing_key="test",
            body=bytes(str(solution.id), encoding="utf-8"),
        )


class Queue(str, Enum):
    test = auto()
    notification = auto()


class QueueAccessor:

    def publish(self, queue: Union[Queue, str], message: Union[bytes, dict]):
        if isinstance(message, dict):
            message = json.dumps(message).encode("UTF-8")
        if isinstance(queue, str):
            queue = Queue(queue)
        with pika.BlockingConnection(
                pika.ConnectionParameters(host=settings.RABBIT_HOST, port=settings.RABBIT_PORT)
        ) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue.name)
            channel.basic_publish(
                exchange="",
                routing_key=queue.name,
                body=message,
            )


def message_handler(queue: Union[Queue, str]):
    if isinstance(queue, str):
        queue = Queue(queue)

    def decorator(func):
        def new_func(*args, **kwargs):
            print("Enter listener for queue", queue)
            with pika.BlockingConnection(
                pika.ConnectionParameters(host=settings.RABBIT_HOST)
            ) as connection:
                channel = connection.channel()
                channel.queue_declare(queue=queue.name)
                channel.basic_consume(queue=queue.name, on_message_callback=func, auto_ack=True)
                channel.start_consuming()
        return new_func
    return decorator
