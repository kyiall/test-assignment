from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
    parent_id: int | None = None
