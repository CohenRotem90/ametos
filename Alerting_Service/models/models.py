from pydantic import BaseModel


class SensorModel(BaseModel):
    device_id: str  # MAC address
    device_type: str


class CommonVarModel(SensorModel):
    super(SensorModel)
    timestamp: str
    event_type: str


class IntrusionDetectionAlert(CommonVarModel):
    super(CommonVarModel)
    zone: str
    confidence: float
    photo_base64: str


class RadarAlert(CommonVarModel):
    super(CommonVarModel)
    speed_kmh: int
    location: str


class AccessControllerAlert(CommonVarModel):
    super(CommonVarModel)
    user_id: str
