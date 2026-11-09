from sqlmodel import SQLModel, Field
from typing import Optional

class ScheduleBase(SQLModel):
    name: str = Field(index=True)
    year: int = Field(index=True)
    grade: int = Field(index=True)
    className: str = Field(index=True)

class Schedule(ScheduleBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

class SchedulePublic(ScheduleBase):
    id: int

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(SQLModel):
    name: str | None = None
    year: int | None = None
    grade: int | None = None
    className: str | None = None
