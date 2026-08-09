import logging
from typing import Optional
from sqlmodel import SQLModel, Field

class PersonBase(SQLModel):
    name: str = Field(index=True)
    birthDate: str = Field(default='1900-01-01', index=True)

class Person(PersonBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

class PersonPublic(PersonBase):
    id: int

class PersonCreate(PersonBase):
    pass

class PersonUpdate(SQLModel):
    name: str | None = None
    birthDate: str | None = None
