from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    address: str = Field(...,)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class BuildingResponse(BuildingBase):
    id: int

    model_config = {"from_attributes": True}
