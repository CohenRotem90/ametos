from pydantic import BaseModel
import re


class SensorModel(BaseModel):
    device_id: str  # MAC address
    device_type: str

    def validate_mac_address(self):
        if not re.match(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$", self.device_id):
            return False
        return True


class CommonVarModel(SensorModel):
    super(SensorModel)
    timestamp: str
    event_type: str


class IntrusionDetectionSensor(CommonVarModel):
    super(CommonVarModel)
    zone: str
    confidence: float
    photo_base64: str


class RadarSensor(CommonVarModel):
    super(CommonVarModel)
    speed_kmh: int
    location: str


class AccessControllerSensor(CommonVarModel):
    super(CommonVarModel)
    user_id: str
