from fastapi import FastAPI, HTTPException
from messageBroker.rabbitmq_consumer import RabbitMQConsumer
from handlers.event_handler import EventHandler
from database.postgreSQL_db import PostgreSQL_db
from cache.redis_cache import RedisCache
from fastapi import Request
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

VALID_GET_KEYS = {"start_time", "end_time", "event_type", "device_type", "device_id", "location", "zone", "user_id"}

# Database, Redis, and RabbitMQ setup

redis_client = RedisCache(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=1)

pg_connection = PostgreSQL_db(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                              host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'))

# Create instances of the classes
rabbitmq_consumer = RabbitMQConsumer(queue_name=os.getenv('RABIT_QUEUE'), host=os.getenv('RABIT_HOST'))
event_handler = EventHandler(pg_connection, redis_client)

# Set the custom callback
rabbitmq_consumer.set_callback(event_handler.on_event_processed)

# Run the RabbitMQ consumer in the background
rabbitmq_consumer.run_in_background()
app = FastAPI()


@app.get("/alerts")
def get_alerts(request: Request, start_time: Optional[str] = None, end_time: Optional[str] = None,
               event_type: Optional[str] = None, device_type: Optional[str] = None, device_id: Optional[str] = None,
               location: Optional[str] = None, zone: Optional[str] = None, user_id: Optional[str] = None):
    query_params = request.query_params.keys()

    # Find invalid keys
    invalid_keys = set(query_params) - VALID_GET_KEYS
    if invalid_keys:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid query parameters provided: {', '.join(invalid_keys)}"
        )
    query, params = PostgreSQL_db.get_query_syntax_and_params(start_time=start_time,
                                                              end_time=end_time,
                                                              event_type=event_type,
                                                              device_type=device_type,
                                                              device_id=device_id,
                                                              location=location,
                                                              zone=zone,
                                                              user_id=user_id)
    data = pg_connection.get_data(query, params)
    return {"data": data}
