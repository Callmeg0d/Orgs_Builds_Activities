from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import verify_api_key, get_current_db
from app.repositories.building_repository import BuildingRepository
from app.schemas.building import BuildingResponse

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("/", response_model=List[BuildingResponse])
async def get_buildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_current_db)
):
    """Получить список всех зданий"""
    repository = BuildingRepository(db)
    buildings = await repository.get_all(skip, limit)
    return [BuildingResponse.model_validate(building) for building in buildings]


@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(
    building_id: int,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_current_db)
):
    """Получить информацию о здании по ID"""
    repository = BuildingRepository(db)
    building = await repository.get(building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здание не найдено"
        )
    return BuildingResponse.model_validate(building)


