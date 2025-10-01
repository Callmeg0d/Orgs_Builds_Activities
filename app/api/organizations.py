from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.dependencies import verify_api_key, get_current_db
from app.services.organization_service import OrganizationService
from app.schemas.organization import OrganizationResponse, OrganizationListResponse

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/", response_model=List[OrganizationListResponse])
async def get_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_current_db)
):
    """Получить список всех организаций"""
    service = OrganizationService(db)
    organizations = await service.organization_repo.get_all(skip, limit)
    return [OrganizationListResponse.model_validate(org) for org in organizations]


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: int,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_current_db)
):
    """Получить информацию об организации по ID"""
    service = OrganizationService(db)
    organization = await service.get_organization(organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организация не найдена"
        )
    return organization


@router.get("/building/{building_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_building(
    building_id: int,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_current_db)
):
    """Получить список всех организаций в конкретном здании"""
    service = OrganizationService(db)
    return await service.get_organizations_by_building(building_id)


@router.get("/activity/{activity_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_activity(
    activity_id: int,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_current_db)
):
    """Получить список всех организаций по виду деятельности"""
    service = OrganizationService(db)
    return await service.get_organizations_by_activity(activity_id)


@router.get("/activity-tree/{activity_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_activity_tree(
    activity_id: int,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_current_db)
):
    """Получить список организаций по дереву деятельности (включая дочерние)"""
    service = OrganizationService(db)
    return await service.get_organizations_by_activity_tree(activity_id)


@router.get("/search/rectangle", response_model=List[OrganizationResponse])
async def get_organizations_in_rectangle(
    min_lat: float = Query(..., ge=-90, le=90),
    max_lat: float = Query(..., ge=-90, le=90),
    min_lon: float = Query(..., ge=-180, le=180),
    max_lon: float = Query(..., ge=-180, le=180),
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_current_db)
):
    """Получить организации в прямоугольной области"""
    service = OrganizationService(db)
    return await service.get_organizations_in_rectangle(min_lat, max_lat, min_lon, max_lon)


@router.get("/search/name", response_model=List[OrganizationResponse])
async def search_organizations_by_name(
    name: str = Query(..., min_length=1),
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_current_db)
):
    """Поиск организаций по названию"""
    service = OrganizationService(db)
    return await service.search_organizations_by_name(name)
