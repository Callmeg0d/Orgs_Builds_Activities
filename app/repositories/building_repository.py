from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.models.building import Building
from app.repositories.base_repository import BaseRepository


class BuildingRepository(BaseRepository[Building]):
    def __init__(self, db: AsyncSession):
        super().__init__(Building, db)

    async def get_with_organizations(self, id: int) -> Optional[Building]:
        result = await self.db.execute(
            select(Building)
            .options(
                selectinload(Building.organizations).selectinload("activities"),
                selectinload(Building.organizations).selectinload("phone_numbers")
            )
            .filter(Building.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all_with_organizations(self, skip: int = 0, limit: int = 100) -> List[Building]:
        result = await self.db.execute(
            select(Building)
            .options(
                selectinload(Building.organizations).selectinload("activities"),
                selectinload(Building.organizations).selectinload("phone_numbers")
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search_by_address(self, address: str) -> List[Building]:
        result = await self.db.execute(
            select(Building).filter(Building.address.ilike(f"%{address}%"))
        )
        return result.scalars().all()
