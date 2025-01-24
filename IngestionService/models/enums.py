from enum import Enum


class EventTypes(str, Enum):
    INTRUSION_DETECTION = "motion_detected"
    RADAR = "speed_violation"
    ACCESS_CONTROLLER = "access_attempt"


class DeviceTypes(str, Enum):
    SECURITY_CAMERA = "security_camera"
    RADAR = "radar,"
    ACCESS_CONTROLLER = "access_controller"
