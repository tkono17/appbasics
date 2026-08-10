import fire
from ..app import DbApp
from ..rdb import RdbAccess
from ..testmodel import (
    Person, PersonPublic, PersonCreate, PersonUpdate
)

def main():
    rdbService = RdbAccess()
    rdbService.addTable('person', Person, PersonPublic, PersonCreate, PersonUpdate)
    dbapp = DbApp()
    dbapp.init(rdbService)
    print('create fire')
    fire.Fire(dbapp)

if __name__ == '__main__':
    main()
