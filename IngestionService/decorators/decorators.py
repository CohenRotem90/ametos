from fastapi import HTTPException
from models.enums import EventTypes, DeviceTypes
from models.models import RadarSensor, IntrusionDetectionSensor, AccessControllerSensor


def transform_event(func):
    def wrapper(event: dict):
        if "event_type" not in event:
            raise HTTPException(status_code=400, detail="Missing 'event_type' in event data")

        event_type = event["event_type"]
        if event_type == EventTypes.INTRUSION_DETECTION:
            event["device_type"] = DeviceTypes.SECURITY_CAMERA
            transformed_event = IntrusionDetectionSensor(**event)
        elif event_type == EventTypes.RADAR:
            event["device_type"] = DeviceTypes.RADAR
            transformed_event = RadarSensor(**event)
        elif event_type == EventTypes.ACCESS_CONTROLLER:
            event["device_type"] = DeviceTypes.ACCESS_CONTROLLER
            transformed_event = AccessControllerSensor(**event)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown event_type: {event_type}")

        return func(transformed_event)

    return wrapper
