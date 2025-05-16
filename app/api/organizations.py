from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.crud.organizations import get_organizations_by_building, get_organizations_by_activity, \
    get_organizations_by_parent_activity, \
    get_organizations_by_name, get_organization_by_id, find_organizations
from app.schemas.organizations import OrganizationResponse, OrganizationActivityResponse, LocationData

router = APIRouter(prefix="/organizations")


@router.get("/by_building", response_model=list[OrganizationResponse])
async def list_organizations_by_building(building: int, db: AsyncSession = Depends(get_db)):
    return await get_organizations_by_building(db, building)


@router.get("/by_activity", response_model=list[OrganizationActivityResponse])
async def list_organizations_by_activity(activity: int, db: AsyncSession = Depends(get_db)):
    return await get_organizations_by_activity(db, activity)


@router.get("/by_parent_activity", response_model=list[OrganizationActivityResponse])
async def list_organizations_by_parent_activity(parent_activity: int, db: AsyncSession = Depends(get_db)):
    return await get_organizations_by_parent_activity(db, parent_activity)


@router.get("/search_by_name", response_model=list[OrganizationResponse])
async def search_organizations_by_name(name: str, db: AsyncSession = Depends(get_db)):
    return await get_organizations_by_name(db, name)


@router.get("/{id}", response_model=OrganizationResponse)
async def get_organization(organization_id: int, db: AsyncSession = Depends(get_db)):
    return await get_organization_by_id(db, organization_id)


@router.post("/nearby", response_model=list[OrganizationResponse])
async def search_organizations(location_data: LocationData, db: AsyncSession = Depends(get_db)):
    return await find_organizations(db, location_data)
