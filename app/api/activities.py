from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.crud.activities import create_activity
from app.schemas.activities import ActivityBase

router = APIRouter(prefix="/activities")


@router.post("", response_model=ActivityBase)
async def add_activity(activity_data: ActivityBase, db: AsyncSession = Depends(get_db)):
    return await create_activity(db, activity_data)
