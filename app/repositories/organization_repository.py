from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import and_, select
from app.models.organization import Organization
from app.models.activity import Activity
from app.models.building import Building
from app.repositories.base_repository import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, db: AsyncSession):
        super().__init__(Organization, db)

    async def get_with_details(self, id: int) -> Optional[Organization]:
        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers)
            )
            .filter(Organization.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_building(self, building_id: int) -> List[Organization]:
        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers)
            )
            .filter(Organization.building_id == building_id)
        )
        return result.scalars().all()

    async def get_by_activity(self, activity_id: int) -> List[Organization]:
        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers)
            )
            .filter(Organization.activities.any(id=activity_id))
        )
        return result.scalars().all()

    async def get_by_activity_tree(self, activity_id: int) -> List[Organization]:
        async def get_all_children(activity_id: int) -> List[int]:
            result = await self.db.execute(select(Activity.id).filter(Activity.parent_id == activity_id))
            children = result.scalars().all()
            result_ids = [activity_id]
            for child in children:
                result_ids.extend(await get_all_children(child))
            return result_ids
        
        activity_ids = await get_all_children(activity_id)
        
        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers)
            )
            .filter(Organization.activities.any(Activity.id.in_(activity_ids)))
        )
        return result.scalars().all()

    async def get_in_rectangle(self, min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> List[Organization]:
        
        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers)
            )
            .join(Organization.building)
            .filter(
                and_(
                    Building.latitude >= min_lat,
                    Building.latitude <= max_lat,
                    Building.longitude >= min_lon,
                    Building.longitude <= max_lon
                )
            )
        )
        return result.scalars().all()

    async def get_all_with_details(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        
        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search_by_name(self, name: str) -> List[Organization]:
        result = await self.db.execute(
            select(Organization)
            .options(
                joinedload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phone_numbers)
            )
            .filter(Organization.name.ilike(f"%{name}%"))
        )
        return result.scalars().all()
