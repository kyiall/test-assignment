from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Building
from app.schemas.buildings import BuildingBase


async def create_building(db: AsyncSession, building_data: BuildingBase):
    point = WKTElement(f'POINT({building_data.longitude} {building_data.latitude})', srid=4326)
    building = Building(
        address=building_data.address,
        location=point
    )
    db.add(building)
    await db.commit()
    await db.refresh(building)
    point = to_shape(building.location)
    return BuildingBase(
        address=building.address,
        latitude=point.y,
        longitude=point.x
    )
