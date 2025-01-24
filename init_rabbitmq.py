import pika
import time

def initialize_rabbitmq():
    max_retries = 10
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq")
            )
            channel = connection.channel()
            channel.queue_declare(queue="events", durable=False)  # Create the 'events' queue
            print("Queue 'events' has been declared.")
            connection.close()
            return
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)  # Wait before retrying
    print("Failed to connect to RabbitMQ after multiple attempts.")
    raise Exception("RabbitMQ initialization failed.")

if __name__ == "__main__":
    initialize_rabbitmq()