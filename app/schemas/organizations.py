from typing import List

from pydantic import BaseModel

from app.schemas.buildings import BuildingSchema


class PhoneNumberBase(BaseModel):
    number: str


class OrganizationResponse(BaseModel):
    name: str
    phone_number: List[PhoneNumberBase]
    building: BuildingSchema


class OrganizationActivityResponse(BaseModel):
    organization: OrganizationResponse


class LocationData(BaseModel):
    latitude: float
    longitude: float
    radius: float
