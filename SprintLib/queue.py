import pika
from django.core.management import BaseCommand
from pika.adapters.utils.connection_workflow import AMQPConnectorException

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


class MessagingSupport(BaseCommand):
    queue_name = None

    def consume(self, ch, method, properties, body):
        raise NotImplementedError

    def handle(self, *args, **options):
        if self.queue_name is None:
            raise NotImplementedError("Queue name must be declared")
        print("start listening " + self.queue_name)
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=settings.RABBIT_HOST)
                )
                channel = connection.channel()
                channel.queue_declare(queue=self.queue_name)
                channel.basic_consume(queue=self.queue_name, on_message_callback=self.consume, auto_ack=True)
                channel.start_consuming()
            except AMQPConnectorException:
                print("connection to rabbit failed: reconnecting")
