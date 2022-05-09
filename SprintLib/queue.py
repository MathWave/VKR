import json

import pika
from django.contrib.auth.models import User
from django.core.management import BaseCommand
import psycopg2
import django.db
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
        data = json.loads(body.decode('utf-8'))
        print(f"Got {data}, processing...")
        try:
            self.process(data)
            print("Process finished successfully")
        except (psycopg2.OperationalError, django.db.OperationalError):
            print("Failed to connect to database, restarting...")
            send_to_queue(self.queue_name, data)
            raise

    def handle(self, *args, **options):
        if self.queue_name is None:
            raise NotImplementedError("Queue name must be declared")
        print("start listening " + self.queue_name)
        while True:
            try:
                with pika.BlockingConnection(
                    pika.ConnectionParameters(host=settings.RABBIT_HOST)
                ) as connection:
                    channel = connection.channel()
                    channel.queue_declare(queue=self.queue_name)
                    channel.basic_consume(queue=self.queue_name, on_message_callback=self.consume, auto_ack=True)
                    channel.start_consuming()
            except AMQPConnectorException:
                print("connection to rabbit failed: reconnecting")


def notify(user: User, notification_type: str, text: str):
    send_to_queue("notifications", {
        'user_id': user.id,
        'type': notification_type,
        'text': text,
    })
