from sqlmodel import SQLModel, Field
from typing import Optional

class CourseBase(SQLModel):
    name: str = Field(index=True)
    description: str | None = Field(default=None, index=True)
    teacher: str | None = Field(default=None, index=True)

class Course(CourseBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

class CoursePublic(CourseBase):
    id: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    teacher: str | None = None
