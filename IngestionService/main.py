from typing import Any
from fastapi import FastAPI, HTTPException
from typing import Optional
from cache.redis_cache import RedisCache
from database.postgreSQL_db import PostgreSQL_db
from messageBroker.rabbitMQ import RabbitMQ
from fastapi import Request
from decorators.decorators import transform_event
from dotenv import load_dotenv
import os

load_dotenv()

VALID_GET_KEYS = {"start_time", "end_time", "event_type", "device_type"}
# Database and Redis initialization
pg_connection = PostgreSQL_db(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                              host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'))

redis_service = RedisCache(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0)


#host, queue):
rabbit = RabbitMQ(queue_name=os.getenv('RABIT_QUEUE'), host=os.getenv('RABIT_HOST'))

app = FastAPI()


@app.post("/events")
@transform_event
def post_event(event: Any):
    cached = redis_service.is_device_in_cache(event.device_id)
    if cached is None:
        is_valid = event.validate_mac_address()
        redis_service.add_device(event, is_valid)
    elif not cached:
        raise HTTPException(status_code=400, detail="event isn't valid")

    # Insert event into PostgreSQL
    pg_connection.send_data(event)
    rabbit.send_object(event)
    return {"message": "Event handled successfully"}


@app.get("/events")
def get_events(request: Request, start_time: Optional[str] = None, end_time: Optional[str] = None,
               event_type: Optional[str] = None, device_type: Optional[str] = None):
    query_params = request.query_params.keys()

    # Find invalid keys
    invalid_keys = set(query_params) - VALID_GET_KEYS
    if invalid_keys:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid query parameters provided: {', '.join(invalid_keys)}"
        )
    query, params = PostgreSQL_db.get_query_syntax_and_params(start_time, end_time, event_type, device_type)

    return {"data": pg_connection.get_data(query, params)}
