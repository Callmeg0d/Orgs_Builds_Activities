from pydantic import BaseModel, Field
from typing import List, Optional


class ActivityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class ActivityResponse(ActivityBase):
    id: int
    parent_id: Optional[int] = None
    level: int = Field(..., description="Уровень вложенности")
    children: List['ActivityResponse'] = []
    parent: Optional['ActivityResponse'] = None

    model_config = {"from_attributes": True}


# Для рекурсивных ссылок
ActivityResponse.model_rebuild()
