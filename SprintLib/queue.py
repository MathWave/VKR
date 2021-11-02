import pika

from Sprint import settings


def send_testing(solution_id):
    with pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBIT_HOST, port=settings.RABBIT_PORT)
    ) as connection:
        channel = connection.channel()
        channel.queue_declare(queue="test")
        channel.basic_publish(exchange="", routing_key="test", body=bytes(str(solution_id), encoding='utf-8'))
