from dataclasses import fields
from pydantic import BaseModel
import typing
from typing import get_args
import logging
from .modelInspection import getModelInspection

log = logging.getLogger(__name__)

Type = typing.Type('Type')

class ModelInspection:
    def __init__(self, T):
        self.T = T
        pass

    def allFieldNames(self) -> list[str]:
        v = []
        return v

    def fieldNamesWithDefaults(self) -> list[str]:
        v = []
        return v

    def summary(self):
        v = {}
        v['type'] = self.T.__name__
        v['allFieldNames'] = self.allFieldNames()
        v['fieldNamesWithDefaults'] = self.fieldNamesWithDefaults()
        return v

    def fieldExists(self, fieldName: str) -> bool:
        v = False
        return v
    
    def fieldTypes(self, fieldName: str) -> list[Type]:
        v = []
        return v

    def fieldHasDefault(self, fieldName: str) -> bool:
        v = False
        return v

    def fieldDefaultValue(self, fieldName: str) -> typing.Any:
        v = None
        return v
    
    def dump(self) -> None:
        pass

class ModelInspection_BaseModel(ModelInspection):
    def __init__(self, T):
        super().__init__(T)
        pass

    def allFieldNames(self) -> list[str]:
        v = []
        if self.T is None:
            pass
        else:
            v = list(self.T.model_fields.keys())
        return v

    def fieldNamesWithDefaults(self) -> list[str]:
        v = []
        if self.T is None:
            pass
        else:
            for name, field in self.T.model_fields.items():
                if field.default is not None or field.default_factory is not None:
                    v.append(name)
        return v

    def dump(self) -> None:
        keys = self.T.model_fields.keys()
        log.info(f'ModelInspection (BaseModel):')
        finspector = None
        for key in keys:
            field = self.T.model_fields[key]
            if finspector is None:
                finspector = getFieldInspection(field)
            log.info(f'  {key}: {field} ({field.__class__.__name__})')

class ModelInspection_dataclass(ModelInspection):
    def __init__(self, T):
        super().__init__(T)
        pass

    def defaultValue(self):
        x = None
        return None
    
    def allFieldNames(self):
        v = []
        if self.T is None:
            pass
        else:
            v = list(self.T.__dataclass_fields__.keys())
        return v

    def dump(self):
        keys = self.T.__dataclass_fields__.keys()
        log.info(f'ModelCheck:')
        for key in keys:
            log.info(f'  {key}: {self.T.__dataclass_fields__[key]}')

def isBaseModel(obj):
    log.info(f'isSqlModel: {dir(obj)}')
    return issubclass(obj, BaseModel)

def getModelInspection(obj) -> ModelInspection:
    if isBaseModel(obj):
        return ModelInspection_BaseModel(obj)
    else:
        return ModelInspection_dataclass(obj)
