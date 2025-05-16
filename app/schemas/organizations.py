from typing import List

from pydantic import BaseModel


class PhoneNumberBase(BaseModel):
    number: str


class OrganizationResponse(BaseModel):
    name: str
    phone_number: List[PhoneNumberBase]


class OrganizationActivityResponse(BaseModel):
    organization: OrganizationResponse


class LocationData(BaseModel):
    latitude: float
    longitude: float
    radius: float
