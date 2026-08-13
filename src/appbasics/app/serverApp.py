import argparse
import logging
import importlib

log = logging.getLogger(__name__)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--app', dest='app',
                        type=str, default='appbasics.dbapp',
                        help='Server application class')
    parser.add_argument('--host', dest='host',
                        type=str, default='localhost',
                        help='Server host')
    parser.add_argument('-p', '--port', dest='port',
                        type=int, default='7601',
                        help='Server port')
    return parser.parse_args()

def createWebApp(app):
    idot = app.rfind('.')
    app = None
    if idot >= 0:
        moduleName = app[:idot]
        clsname = app[idot+1:]
        module = importlib.import_module(moduleName)
        if module is not None and hasattr(module, clsname):
            cls = getattr(module, clsname)
            log.info(f'  Successfully obtained application class {clsname} from {moduleName}')
            app = cls()
        else:
            log.warning(f'  Failed to import module {moduleName}')
    return app
    
def main():
    args = parseArgs()
    app = createApp(args.app)
    app()

if __name__ == '__main__':
    main()
