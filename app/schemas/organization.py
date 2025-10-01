from pydantic import BaseModel, Field
from typing import List


class PhoneNumberResponse(BaseModel):
    id: int
    number: str

    model_config = {"from_attributes": True}


class ActivitySimpleResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Название организации")
    building_id: int = Field(..., description="ID здания")


class OrganizationListResponse(BaseModel):
    id: int
    name: str
    building_id: int

    model_config = {"from_attributes": True}


class OrganizationResponse(OrganizationBase):
    id: int
    phone_numbers: List[PhoneNumberResponse] = []
    activities: List[ActivitySimpleResponse] = []

    model_config = {"from_attributes": True}
