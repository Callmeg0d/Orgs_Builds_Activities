from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.organization import OrganizationResponse


class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.organization_repo = OrganizationRepository(db)

    async def get_organization(self, organization_id: int) -> Optional[OrganizationResponse]:
        organization = await self.organization_repo.get_with_details(organization_id)
        if not organization:
            return None
        
        organization_data = {
            "id": organization.id,
            "name": organization.name,
            "building_id": organization.building_id,
            "phone_numbers": [
                {"id": phone.id, "number": phone.number} 
                for phone in organization.phone_numbers
            ],
            "activities": [
                {"id": activity.id, "name": activity.name}
                for activity in organization.activities
            ]
        }
        return OrganizationResponse.model_validate(organization_data)

    async def get_organizations_by_building(self, building_id: int) -> List[OrganizationResponse]:
        organizations = await self.organization_repo.get_by_building(building_id)
        return [OrganizationResponse.model_validate(org) for org in organizations]

    async def get_organizations_by_activity(self, activity_id: int) -> List[OrganizationResponse]:
        organizations = await self.organization_repo.get_by_activity(activity_id)
        return [OrganizationResponse.model_validate(org) for org in organizations]

    async def get_organizations_by_activity_tree(self, activity_id: int) -> List[OrganizationResponse]:
        organizations = await self.organization_repo.get_by_activity_tree(activity_id)
        return [OrganizationResponse.model_validate(org) for org in organizations]

    async def get_organizations_in_rectangle(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> List[OrganizationResponse]:
        organizations = await self.organization_repo.get_in_rectangle(min_lat, max_lat, min_lon, max_lon)
        return [OrganizationResponse.model_validate(org) for org in organizations]

    async def search_organizations_by_name(self, name: str) -> List[OrganizationResponse]:
        organizations = await self.organization_repo.search_by_name(name)
        return [OrganizationResponse.model_validate(org) for org in organizations]

