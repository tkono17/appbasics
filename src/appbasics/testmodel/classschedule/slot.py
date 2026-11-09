from sqlmodel import SQLModel, Field
from typing import Optional

class SlotBase(SQLModel):
    dayOfWeek: int = Field(index=True)
    number: int = Field(index=True)
    courseId: int = Field(index=True)

class Slot(SlotBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

class SlotPublic(SlotBase):
    id: int

class SlotCreate(SlotBase):
    pass

class SlotUpdate(SQLModel):
    dayOfWeek: int | None = None
    number: int | None = None
    courseId: int | None = None
