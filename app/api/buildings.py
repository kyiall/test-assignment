from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.crud.buildings import create_building
from app.schemas.buildings import BuildingBase

router = APIRouter(prefix="/buildings")


@router.post("", response_model=BuildingBase)
async def add_building(building_data: BuildingBase, db: AsyncSession = Depends(get_db)):
    return await create_building(db, building_data)



