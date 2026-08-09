from sqlmodel import SQLModel, Field
import appbasics as ab

class PersonBase(SQLModel):
    name: str = Field(index=True)
    age: int = Field(default=0, index=True)

class Person(PersonBase, table=True):
    id: int = Field(primary_key=True)

class PersonPublic(PersonBase):
    id: int

class PersonCreate(PersonBase):
    pass

class PersonUpdate(PersonBase):
    name: str | None = None
    age: int | None = None

def test_person():
    table = ab.TableAccess(Person, PersonPublic, PersonCreate, PersonUpdate)
