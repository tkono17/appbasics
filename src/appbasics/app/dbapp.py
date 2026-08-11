import os
import dotenv
import logging
from sqlmodel import SQLModel
from ..rdb import RdbAccess

log = logging.getLogger(__name__)

# Make RdbAccess service as an application
class DbApp:
    def __init__(self):
        self.rdbService = None
        self.tableItems = {}
        self.currentTableItem = {}

    def init(self, rdbService: RdbAccess):
        self.rdbService = rdbService
        dotenv.load_dotenv('.env')
        print(os.environ)
        if 'DB_URL' in os.environ:
            db_url = os.environ['DB_URL']
            print('connected')
            self.rdbService.connectDb(db_url)

    def initDb(self):
        if self.rdbService is not None:
            SQLModel.metadata.create_all(self.rdbService.engine)

    def create(self, tableName: str, **kwargs):
        if self.rdbService is None:
            raise Exception("RdbAccess service is not initialized.")
        x = self.rdbService.create(tableName, kwargs)
        if x is not None:
            log.info(f'  created {tableName} {x}')
            self.tableItems[tableName] = [x]
            self.currentTableItem[tableName] = x
        else:
            self.tableItems[tableName] = []
            self.currentTableItem[tableName] = None

    def update(self, tableName: str, id: int, **kwargs):
        if self.rdbService is None:
            raise Exception("RdbAccess service is not initialized.")
        x = self.rdbService.update(tableName, id, kwargs)
        if x is not None:
            log.info(f'  update id={id} -> {x}')
            self.tableItems[tableName] = [x]
            self.currentTableItem[tableName] = x
        else:
            log.info(f'  update id={id} -> failed')
            self.tableItems[tableName] = []
            self.currentTableItem[tableName] = None

    def get(self, tableName: str, id: int):
        if self.rdbService is None:
            raise Exception("RdbAccess service is not initialized.")
        x = self.rdbService.get(tableName, id)
        if x is not None:
            log.info(f'  get id={id} -> {x}')
            self.tableItems[tableName] = [x]
            self.currentTableItem[tableName] = x
        else:
            log.info(f'  get id={id} -> nothing returned')
            self.tableItems[tableName] = []
            self.currentTableItem[tableName] = None
        
    def getall(self, tableName: str, **kwargs):
        if self.rdbService is None:
            raise Exception("RdbAccess service is not initialized.")
        v = self.rdbService.getall(tableName, **kwargs)
        if v is not None:
            log.info(f'  getall {tableName} -> {len(v)} items')
            for i, item in enumerate(v):
                log.info(f'    item[{i}]: {item}')
            self.tableItems[tableName] = v
            if v and len(v) == 1:
                self.currentTableItem[tableName] = v[0]
            else:
                self.currentTableItem[tableName] = None
        else:
            log.info(f'  getall {tableName} -> nothing returned')
            self.tableItems[tableName] = []
            self.currentTableItem[tableName] = None

    def delete(self, tableName: str, id: int):
        if self.rdbService is None:
            raise Exception("RdbAccess service is not initialized.")
        status = self.rdbService.delete(tableName, id)
        if status == 0:
            log.info(f'  delete {tableName} id={id} -> done')
            v1 = self.tableItems[tableName] if tableName in self.tableItems else []
            x1 = self.currentTableItem[tableName] if tableName in self.currentTableItem else None
            self.tableItems[tableName] = [ x for x in v1 if x.id != id ]
            self.currentTableItem[tableName] = None if x1 is None else x1 if x1.id == id else x1
