import argparse
import logging
import importlib
import uvicorn

log = logging.getLogger(__name__)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--appPath', dest='app',
                        type=str, default='appbasics.dbapp:main',
                        help='Server application class')
    parser.add_argument('--host', dest='host',
                        type=str, default='localhost',
                        help='Server host')
    parser.add_argument('-p', '--port', dest='port',
                        type=int, default='7601',
                        help='Server port')
    parser.add_argument('-l', '--log-level', dest='logLevel',
                        type=str, default='INFO',
                        help='Log level (DEBUG|INFO|WARNING|ERROR)')
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

def stringToLogLevel(sloglevel: str):
    level = logging.INFO
    match sloglevel:
        case 'DEBUG': level = logging.DEBUG
        case 'INFO': level = logging.INFO
        case 'WARNING': level = logging.WARNING
        case 'ERROR': level = logging.ERROR
    return level

def startServer(appPath: str, host: str, port: int, log_level: str = 'INFO'):
    logging.basicConfig(level=stringToLogLevel(log_level))
    config = uvicorn.Config(appPath, host=host, port=port, log_level='info')
    server = uvicorn.Server(config)
    server.run()

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(name)-20s %(levelname)-8s %(message)s')
    args = parseArgs()
    if args.appPath != '':
        startServer(args.appPath, host=args.host, port=args.port, log_level=args.logLevel)
    else:
        log.warning(f'Application path {args.appPath} is empty')

if __name__ == '__main__':
    main()
