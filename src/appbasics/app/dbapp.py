import os
import dotenv
from sqlmodel import SQLModel
from ..rdb import RdbAccess

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
        v = self.rdbService.create(tableName, kwargs)
        if v is not None and len(v) == 1:
            self.tableItems[tableName] = v
            self.currentTableItem[tableName] = v[0]
        else:
            self.tableItems[tableName] = []
            self.currentTableItem[tableName] = None

    def update(self, tableName: str, id: int, **kwargs):
        if self.rdbService is None:
            raise Exception("RdbAccess service is not initialized.")
        v = self.rdbService.update(tableName, id, kwargs)
        if v is not None and len(v) == 1:
            self.tableItems[tableName] = v
            self.currentTableItem[tableName] = v[0]
        else:
            self.tableItems[tableName] = []
            self.currentTableItem[tableName] = None

    def get(self, tableName: str, id: int):
        if self.rdbService is None:
            raise Exception("RdbAccess service is not initialized.")
        v = self.rdbService.get(tableName, id)
        if v is not None and len(v) == 1:
            self.tableItems[tableName] = v
            self.currentTableItem[tableName] = v[0]
        else:
            self.tableItems[tableName] = []
            self.currentTableItem[tableName] = None
        
    def getall(self, tableName: str, **kwargs):
        if self.rdbService is None:
            raise Exception("RdbAccess service is not initialized.")
        v = self.rdbService.getall(tableName, **kwargs)
        if v is not None:
            self.tableItems[tableName] = v
            if v and len(v) == 1:
                self.currentTableItem[tableName] = v[0]
            else:
                self.currentTableItem[tableName] = None
        else:
            self.tableItems[tableName] = []
            self.currentTableItem[tableName] = None

    def delete(self, tableName: str, id: int):
        if self.rdbService is None:
            raise Exception("RdbAccess service is not initialized.")
        status = self.rdbService.delete(tableName, id)
        if status == 0:
            v1 = self.tableItems[tableName]
            x1 = self.currentTableItem[tableName]
            self.tableItems[tableName] = [ x for x in v1 if x.id != id ]
            self.currentTableItem[tableName] = None if x1.id == id else x1

