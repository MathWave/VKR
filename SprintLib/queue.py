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
