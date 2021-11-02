import pika
from django.core.management.base import BaseCommand

from Main.models import Solution
from Sprint import settings
from SprintLib.testers import *


class Command(BaseCommand):
    help = 'Tests solution'

    def handle(self, *args, **options):
        print("Enter worker")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_HOST))
        channel = connection.channel()
        channel.queue_declare(queue='test')

        def callback(ch, method, properties, body):
            try:
                id = int(str(body, encoding='utf-8'))
                print(f"Received id {id}")
                solution = Solution.objects.get(id=id)
            except:
                return
            try:
                eval(solution.language.work_name + 'Tester')(solution).execute()
            except:
                solution.result = 'TE'
                solution.save()

        channel.basic_consume(queue='test', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
