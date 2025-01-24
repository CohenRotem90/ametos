import pika
import threading


class RabbitMQConsumer:
    def __init__(self, queue_name: str, host: str = "localhost"):
        self.queue_name = queue_name
        self.host = host
        self.connection = None
        self.channel = None
        self.callback = None  # Custom callback function

    def set_callback(self, callback):
        """
        Set a custom callback to trigger when a message is processed.
        """
        self.callback = callback

    def process_message(self, ch, method, properties, body):

        print(f"Processing message: {body.decode()}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

        if self.callback:
            self.callback(body.decode())

    def start_consumer(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=False)

        print(f"Listening for messages on queue: {self.queue_name}")

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_message
        )

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("Stopping consumer...")
            self.channel.stop_consuming()

        self.connection.close()

    def run_in_background(self):
        consumer_thread = threading.Thread(target=self.start_consumer)
        consumer_thread.daemon = True
        consumer_thread.start()
