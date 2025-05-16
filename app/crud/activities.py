from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import CustomError
from app.models import Activity
from app.schemas.activities import ActivityBase


async def create_activity(db: AsyncSession, activity_data: ActivityBase):
    level = 1

    if activity_data.parent_id:
        query = select(Activity).where(Activity.id == activity_data.parent_id)
        result = await db.execute(query)
        parent = result.scalar_one_or_none()

        if not parent:
            raise CustomError(status_code=404, name="Родитель не найден")

        if parent.level >= 3:
            raise CustomError(status_code=400, name="Превышен максимально допустимый уровень (3)")

        level = parent.level + 1

    new_activity = Activity(name=activity_data.name, parent_id=activity_data.parent_id, level=level)
    db.add(new_activity)
    await db.commit()
    await db.refresh(new_activity)
    return new_activity
