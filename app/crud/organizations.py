from geoalchemy2.functions import ST_DWithin, ST_Point
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, OrganizationActivity, Activity, Building
from app.schemas.organizations import LocationData


async def get_organizations_by_building(db: AsyncSession, building: int):
    query = select(Organization).where(Organization.building_id == building)
    result = await db.execute(query)
    return result.scalars().all()


async def get_organizations_by_activity(db: AsyncSession, activity: int):
    query = select(OrganizationActivity).where(OrganizationActivity.activity_id == activity)
    result = await db.execute(query)
    return result.scalars().all()


async def get_organizations_by_parent_activity(db: AsyncSession, parent_activity: int):
    query = (
        select(OrganizationActivity)
            .join(Activity, OrganizationActivity.activity_id == Activity.id)
            .where(Activity.parent_id == parent_activity)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_organizations_by_name(db: AsyncSession, name: str):
    query = select(Organization).where(Organization.name.ilike(f"%{name}%"))
    result = await db.execute(query)
    return result.scalars().all()


async def get_organization_by_id(db: AsyncSession, organization_id: int):
    organization = (await db.scalars(select(Organization).where(Organization.id == organization_id))).first()
    return organization


async def find_organizations(db: AsyncSession, location_data: LocationData):
    query = select(Building).where(
        ST_DWithin(
            Building.location,
            ST_Point(location_data.longitude, location_data.latitude),
            location_data.radius
        )
    )
    result = await db.execute(query)
    buildings = result.scalars().all()
    building_ids = [building.id for building in buildings]
    organizations = select(Organization).where(Organization.building_id.in_(building_ids))
    result = await db.execute(organizations)
    return result.scalars().all()
