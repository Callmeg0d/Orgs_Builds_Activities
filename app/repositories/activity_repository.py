from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select
from app.models.activity import Activity
from app.repositories.base_repository import BaseRepository


class ActivityRepository(BaseRepository[Activity]):
    def __init__(self, db: AsyncSession):
        super().__init__(Activity, db)

    async def get_with_children(self, id: int) -> Optional[Activity]:
        result = await self.db.execute(
            select(Activity)
            .options(
                selectinload(Activity.children),
                joinedload(Activity.parent)
            )
            .filter(Activity.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all_with_relations(self, skip: int = 0, limit: int = 100) -> List[Activity]:
        result = await self.db.execute(
            select(Activity)
            .options(
                selectinload(Activity.children),
                joinedload(Activity.parent)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_root_activities(self) -> List[Activity]:
        """Получить все корневые активности (без родителя)"""
        result = await self.db.execute(
            select(Activity).filter(Activity.parent_id.is_(None))
        )
        return result.scalars().all()

    async def get_children(self, parent_id: int) -> List[Activity]:
        """Получить всех детей активности"""
        result = await self.db.execute(
            select(Activity).filter(Activity.parent_id == parent_id)
        )
        return result.scalars().all()

    async def get_all_children_recursive(self, parent_id: int) -> List[Activity]:
        """Получить всех потомков активности"""
        async def get_children_recursive(activity_id: int) -> List[Activity]:
            children = await self.get_children(activity_id)
            result = children.copy()
            for child in children:
                result.extend(await get_children_recursive(child.id))
            return result
        
        return await get_children_recursive(parent_id)
