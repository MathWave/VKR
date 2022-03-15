import json

import pika
from django.core.management import BaseCommand
from pika.adapters.utils.connection_workflow import AMQPConnectorException

from Sprint import settings


def send_to_queue(queue_name, payload):
    with pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBIT_HOST, port=settings.RABBIT_PORT)
    ) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(payload).encode('utf-8'),
        )


class MessagingSupport(BaseCommand):
    queue_name = None

    def process(self, payload: dict):
        raise NotImplementedError

    def consume(self, ch, method, properties, body):
        self.process(json.loads(body.decode('utf-8')))

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
