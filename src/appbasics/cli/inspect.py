import dataclasses
from importlib import import_module
import logging
import typer
from ..dtypes import getTypeInspection, FieldInspection

log = logging.getLogger(__name__)

app = typer.Typer()


@app.command('type')
def inspectType(typeName: str):
    log.info(f'Inspecting type: {typeName}')
    module_name, class_name = typeName.rsplit('.', 1)
    module = import_module(module_name)
    cls = getattr(module, class_name)
    log.info(f'  Class: {cls}')
    log.info(f'    {cls.model_fields}')
    tinspector = getTypeInspection(cls)
    tinspector.dump()

@app.command('field')
def inspectField(fieldName: str):
    log.info(f'Inspecting field: {fieldName}')
    module_name, class_name, field_name = fieldName.rsplit('.', 2)
    module = import_module(module_name)
    cls = getattr(module, class_name)
    log.info(f'  Class: {cls}')
    field = dataclasses.fields(cls)[field_name]
    finspector = FieldInspection(field)
    finspector.dump()

def main():
    logging.basicConfig(level=logging.INFO, format='%(name)-20s %(levelname)-8s %(message)s')
    app()

if __name__ == "__main__":
    main()
