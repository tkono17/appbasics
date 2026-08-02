import logging
from typing import Optional
from sqlmodel import Session, select, Engine

log = logging.getLogger(__name__)

dbEngine = None
def setEngine(engine):
    global dbEngine
    dbEngine = engine

def getEngine():
    global dbEngine
    return dbEngine


class TableAccess[TDb, TPublic, TCreate, TUpdate]:
    def __init__(self, tdb: type[TDb], 
                 tpublic: type[TPublic], 
                 tcreate: type[TCreate], 
                 tupdate: type[TUpdate]):
        self.TDb = tdb
        self.TPublic = bpublic
        self.TCreate = tcreate
        self.TUpdate = tupdate

    def create(self, data: TCreate, engine: Engine) -> TPublic:
        data_db = self.TDb.model_validate(data)
        with Session(engine) as session:
            log.info(f'  create {type(data_db)} {data_db}')
            session.add(data_db)
            session.commit()
            session.refresh(data_db)
            log.info(f'  created {data_db}')
        return data_db

    def get(self, id: int, engine: Engine) -> TPublic:
        data = None
        with Session(engine) as session:
            data = session.get(self.TDb, id)
        return data
    
    def getall(self, engine: Engine, selectModifier=None, 
               offset: int = 0, limit: int = 100) -> list[TPublic]:
        statement = select(self.TDb).offset(offset).limit(limit)
        #log.info(f'statement (before modify): {statement}')
        if selectModifier is not None:
            statement = selectModifier(statement)
            #log.info(f'statement (after modify): {statement}')
        v = []
        with Session(engine) as session:
            results = session.exec(statement)
            v = results.all()
        return v
    
    def getone(self, engine: Engine, selectModifier=None) -> Optional[TPublic]:
        statement = select(self.TDb)
        if selectModifier is not None:
            statement = selectModifier(statement)
        x = None
        with Session(engine) as session:
            results = session.exec(statement)
            v = results.all()
            log.info(f'  results: {v}')
            x = v[0]
        return x
    
    def update(self, id: int, data: TUpdate, engine: Engine) -> TPublic:
        data_db = self.get(id)
        if data_db is None:
            log.warning(f'Entry id={id} not found in {self.TDb.__name__}')
            return None
        data_update = data.model_dump(exclude_unset=True)
        data_db.sqlmodel_update(data_update)
        with Session(engine) as session:
            session.add(data_db)
            session.commit()
            session.refresh(data_db)
        return data_db
    
    def delete(self, id: int, engine: Engine) -> Optional[int]:
        data_db = self.get(id)
        if data_db is None:
            log.warning(f'Entry id={id} not found in {self.TDb.__name__}')
            return None
        with Session(engine) as session:
            session.delete(data_db)
            session.commit()
        return 0

    def exec(self, statement, engine: Engine, offset: int=0, limit: int=100):
        v = None
        with Session(engine) as session:
            v = session.exec(statement).all()
        return v
