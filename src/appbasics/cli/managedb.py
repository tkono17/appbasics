import os
import typer
import dotenv
import logging
from sqlmodel import SQLModel, create_engine, Session
from ..testmodel import Person, PersonPublic, PersonCreate, PersonUpdate
from ..rdb import RdbAccess, TableAccess

log = logging.getLogger(__name__)

app = typer.Typer()

@app.command('createDb')
def createDb():
    db_url = f'sqlite:///{os.getenv("DB_FILE", "testmodel.db")}'
    log.info(f'Initializing database: {db_url}')
    engine = create_engine(db_url, echo=True)
    SQLModel.metadata.create_all(engine)
    log.info(f'  created database tables: {SQLModel.metadata.tables.keys()}')

def init() -> RdbAccess:
    db_url = f'sqlite:///{os.getenv("DB_FILE", "testmodel.db")}'
    db = RdbAccess()
    db.connectDb(db_url)
    db.addTable('person', Person, PersonPublic, PersonCreate, PersonUpdate)
    return db

@app.command('create-person')
def createPerson(name: str, birthDate: str):
    db = init()
    log.info(f'Creating person {name} with birthDate {birthDate}')
    db.create('person', {'name': name, 'birthDate': birthDate})

@app.command('list-persons')
def listPersons():
    db = init()
    persons = db.getall('person')
    for p in persons:
        log.info(f'Person: {p.id}, {p.name}, {p.birthDate}')    

@app.command('get-person')
def getPerson(id: int):
    db = init()
    person = db.get('person', id)
    if person:
        log.info(f'Found person: {person.id}, {person.name}, {person.birthDate}')
    else:
        log.warning(f'Person with id {id} not found')

@app.command('update-person')
def updatePerson(id: int, name: str | None = None, birthDate: str | None = None):
    db = init()
    kv = {}
    if name is not None: kv['name'] = name
    if birthDate is not None: kv['birthDate'] = birthDate
    db.update('person', id, kv)

@app.command('delete-person')
def deletePerson(id: int):
    db = init()
    result = db.delete('person', id)
    if result == -1:
        log.warning(f'Person with id {id} not found')
    else:
        log.info(f'Deleted person with id {id}')


def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)-8s %(message)s')
    dotenv.load_dotenv()
    app()

if __name__ == '__main__':
    main()
