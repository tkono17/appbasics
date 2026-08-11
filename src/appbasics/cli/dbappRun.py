import fire
import logging
from ..app import DbApp
from ..rdb import RdbAccess
from ..testmodel import (
    Person, PersonPublic, PersonCreate, PersonUpdate
)

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(name)-20s %(levelname)-8s %(message)s')
    rdbService = RdbAccess()
    rdbService.addTable('person', Person, PersonPublic, PersonCreate, PersonUpdate)
    dbapp = DbApp()
    dbapp.init(rdbService)
    print('create fire')
    fire.Fire(dbapp)

if __name__ == '__main__':
    main()
