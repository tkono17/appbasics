from typing import TypeVar
import logging
from sqlmodel import create_engine
from dataclasses import dataclass
from .tableAccess import TableAccess, setEngine

log = logging.getLogger(__name__)

Cls = TypeVar('Cls')

class RdbAccess:
    def __init__(self):
        self.engine = None
        self.tables = {}

    def connectDb(self, url: str):
        log.info(f'Connecting to database {url}')
        # connect_args = {
        #     'check_same_thread': False
        # }
        self.engine = create_engine(url)

    def addTable[TDb, TPublic, TCreate, TUpdate](self, 
                                                 tablename: str, 
                                                 tdb: type[TDb], 
                                                 tpublic: type[TPublic],
                                                 tcreate: type[TCreate]|None = None, 
                                                 tupdate: type[TUpdate]|None = None):
        if tcreate is None: tcreate = tdb
        if tupdate is None: tupdate = tdb
        self.tables[tablename] = TableAccess(tdb, tpublic, tcreate, tupdate)
        
    def getTable(self, tablename):
        table = None
        if tablename in self.tables.keys():
            table = self.tables[tablename]
        return table
        
    def create(self, tablename, keyValues):
        table = self.getTable(tablename)
        tcreate = table.TCreate
        data = None
        if table is not None:
            data = table.create(tcreate(**keyValues), engine=self.engine)
        else:
            log.warning(f'  Cannot create entry in table {tablename}, table not found')
        return data

    def get(self, tablename: str, id: int):
        table = self.getTable(tablename)
        data = None
        if table is not None:
            data = table.get(id, engine=self.engine)
        else:
            log.warning(f'  Cannot get entry {id} in table {tablename}, table not found')
        return data

    def getall(self, tablename: str, selectModifier=None, offset: int=0, limit: int=100):
        table = self.getTable(tablename)
        data = None
        log.info(f'call getall: {table}')
        if table is not None:
            log.info(f'call getall: {tablename}')
            data = table.getall(selectModifier, engine=self.engine, offset, limit)
        else:
            log.warning(f'  Cannot get entries in table {tablename}, table not found')
        return data

    def getone(self, tablename: str, selectModifier=None):
        table = self.getTable(tablename)
        data = None
        if table is not None:
            data = table.getone(selectModifier, engine=self.engine)
        else:
            log.warning(f'  Cannot get entries in table {tablename}, table not found')
        return data

    def update(self, tablename, id, keyValues):
        table = self.getTable(tablename)
        TUpdate = table.TUpdate
        data = None
        if table is not None:
            data = table.update(id, TUpdate(**keyValues), engine=self.engine)
        else:
            log.warning(f'  Cannot update entry {id} in table {tablename}, table not found')
        return data
    
    def delete(self, tablename: str, id: int):
        table = self.getTable(tablename)
        if table is not None:
            table.delete(id, engine=self.engine)
        else:
            log.warning(f'  Cannot get entry {id} in table {tablename}, table not found')
        return 0
    