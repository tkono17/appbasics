from typing import TypeVar, Optional
from dataclasses import dataclass
from sqlmodel import Session, select

TDb = TypeVar('TDb')
TPublic = TypeVar('TPublic')
TCreate = TypeVar('TCreate')
TUpdate = TypeVar('TUpdate')

ClsDb = TypeVar('ClsDb')
ClsPublic = TypeVar('ClsPublic')
ClsCreate = TypeVar('ClsCreate')
ClsUpdate = TypeVar('ClsUpdate')

@dataclass
class DbCrud:
    def __init__(self, ClsDb, ClsPublic, ClsCreate, ClsUpdate, 
                 session: Session):
        self.TDb = ClsDb
        self.TPublic = ClsPublic
        self.TCreate = ClsCreate
        self.TUpdate = ClsUpdate
        self.session - session

    def create(self, data: TCreate, session: SessionDep) -> TPublic:
        return data

    def getall(self) -> list[TPublic]:
        return []

    def get(self, id: int) -> Optional[TPublic]:
        return None
    
    def update(self, id: int, data_update: TUpdate) -> TPublic:
        return TPublic()
    
    def delete(self, id: int):
        return
    
class DbCrudT(DbCrud):
    def __init__(self, session: Session):
        super().__init__(session)

    def create(self, data: TCreate) -> TPublic:
        data_db = self.TDb.model_validate(data)
        self.session.add(data_db)
        self.session.commit()
        self.session.refresh(data_db)
        return data_db

    def getall(self, offset: int = None, limit: int = None) -> list[TPublic]:
        v = self.session.exec(select(TDb).offset(offset).limit(limit)).all()
        return v

    def get(self, id: int) -> Optional[TPublic]:
        data = self.session.get(self.TDb, id)
        if not data:
            raise HTTPException(status_code=404, detail=f"Data not found {id}")
        return data
    
    def update(self, id: int, data_update: TUpdate) -> TPublic:
        data_db = self.session.get(self.TDb, id)
        if not data:
            raise HTTPException(status_code=404, detail=f"Data not found {id}")
        data = data_update.model_dump(exclude_unset=True)
        data_db.sqlmodel_update(data)
        self.session.add(data_db)
        self.session.commit()
        self.session.refresh(data_db)
        return data_db
    
    def delete(self, id: int):
        data = self.session.get(self.TDb, id)
        if not data:
            raise HTTPException(status_code=404, detail=f"Data not found {id}")
        self.session.delete(data)
        self.session.commit()
        return { 'ok': True }
