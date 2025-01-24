from database.postgreSQL_db import PostgreSQL_db
from cache.redis_cache import RedisCache
from models.enums import DeviceTypes
import json
from typing import Optional
from models.models import RadarAlert, IntrusionDetectionAlert, AccessControllerAlert

MAX_SPEED = 90
RESTRICTED = "Restricted Area"


class EventHandler:
    def __init__(self, db_connection: PostgreSQL_db, redis_client: RedisCache):
        self.db_connection = db_connection
        self.redis_client = redis_client

    @staticmethod
    def _get_device_type(device_type: str) -> Optional[DeviceTypes]:
        try:
            # Use the enum's value directly for matching
            return DeviceTypes(device_type)
        except ValueError:
            # Return None if no match is found
            return None

    def _check_radar_event(self, data):
        captured_speed = data["speed_kmh"]
        if captured_speed > MAX_SPEED:
            radar_alert = RadarAlert(**data)
            self.db_connection.send_alert_data(table="alerts", alert=radar_alert)

    def _check_security_camera_event(self, data):
        restricted_zone = data["zone"]
        if restricted_zone == RESTRICTED:
            restricted_alert = IntrusionDetectionAlert(**data)
            self.db_connection.send_alert_data(table="alerts", alert=restricted_alert)

    def _check_access_controller_event(self, data):
        user_id = data["user_id"]
        if not self.redis_client.validate_user(user_id):
            #check on db is user is valid
            if not self.db_connection.is_authorized(user_id):
                access_controller = AccessControllerAlert(**data)
                self.db_connection.send_alert_data(table="alerts", alert=access_controller)
            else:
                self.redis_client.add_validated_user(user_id)

    def on_event_processed(self, message):
        """
        Triggered when a message is processed by the RabbitMQ consumer.
        """

        data_dict = json.loads(message)

        device_type = self._get_device_type(data_dict["device_type"])

        if device_type == DeviceTypes.RADAR:
            self._check_radar_event(data_dict)
        elif device_type == DeviceTypes.ACCESS_CONTROLLER:
            self._check_access_controller_event(data_dict)
        elif device_type == DeviceTypes.SECURITY_CAMERA:
            self._check_security_camera_event(data_dict)
