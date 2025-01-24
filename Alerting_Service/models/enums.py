from enum import Enum


class DeviceTypes(str, Enum):
    SECURITY_CAMERA = "security_camera"
    RADAR = "radar"
    ACCESS_CONTROLLER = "access_controller"
