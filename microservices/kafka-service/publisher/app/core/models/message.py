from typing import Optional
from typing_extensions import TypedDict

from pydantic import BaseModel


class Message(BaseModel):
    name: str
    description: Optional[str] = None
    topic: str


class Email(BaseModel):
    topic: str
    from_: str
    to: str
    subject: str
    message: str
    Service_Type: str


class Location(TypedDict):
    lat: float
    lng: float


class Destination(TypedDict):
    id: str
    location: Location


class AlertData(TypedDict):
    type: str
    priority: str
    alert: bool


class BeaconData(TypedDict):
    timestamp: str
    location: Location
    make: str


class AckData(TypedDict):
    timestamp: str
    location: Location
    make: str
    responding: bool
    destination: Destination


class AlertRequest(BaseModel):
    type: str
    source: str
    id: str
    data: AlertData


class BeaconRequest(BaseModel):
    type: str
    source: str
    id: str
    data: BeaconData


class AckRequest(BaseModel):
    type: str
    source: str
    id: str
    data: AckData
