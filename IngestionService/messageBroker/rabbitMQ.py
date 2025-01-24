import pika
import json


class RabbitMQ:
    def __init__(self, host, queue_name):
        self.host = host
        self.queue_name = queue_name

    def send_object(self, event):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        message = json.dumps(event.__dict__)
        channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        print(f" [x] Sent {event}")
        connection.close()
