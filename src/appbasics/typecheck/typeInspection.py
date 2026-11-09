from dataclasses import fields
from pydantic import BaseModel
import typing
from typing import get_args, TypeVar
import logging

log = logging.getLogger(__name__)

class TypeInspection:
    def __init__(self, T):
        self.T = T
        pass

    def allFieldNames(self) -> list[str]:
        v = []
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

    def summary(self):
        v = {}
        v['type'] = self.T.__name__
        v['allFieldNames'] = self.allFieldNames()
        v['fieldNamesWithDefaults'] = self.fieldNamesWithDefaults()
        return v

    def fieldNamesWithDefaults(self) -> list[str]:
        v = []
        all_names = self.allFieldNames()
        for fieldName in all_names:
            if self.fieldHasDefault(fieldName):
                v.append(fieldName)
        return v
    
    def dataCreate(self) -> dict:
        v = {}
        for fieldName in self.allFieldNames():
            if not self.fieldHasDefault(fieldName):
                v[fieldName] = None
        for fieldName in self.allFieldNames():
            if self.fieldHasDefault(fieldName):
                v[fieldName] = self.fieldDefaultValue(fieldName)
        return v

    def dataUpdate(self) -> dict:
        v = {}
        for fieldName in self.allFieldNames():
            v[fieldName] = None
        return v
    
    def dump(self) -> None:
        info = self.summary()
        for key in info:
            log.info(f'{key}: {info[key]}')

class TypeInspection_BaseModel(TypeInspection):
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

    def fieldTypes(self, fieldName: str) -> list[Type]:
        v = []
        if self.T is None:
            pass
        else:
            field = self.T.model_fields.get(fieldName)
            if field is not None:
                v = get_args(field.annotation)
        return v

    def fieldHasDefault(self, fieldName: str) -> bool:
        v = False
        if self.T is None:
            pass
        else:
            field = self.T.model_fields.get(fieldName)
            if field is not None:
                v = field.default is not None or field.default_factory is not None
        return v

    def fieldDefaultValue(self, fieldName: str) -> typing.Any:
        v = None
        if self.T is None:
            pass
        elif self.fieldHasDefault(fieldName):
            field = self.T.model_fields.get(fieldName)
            if field is not None:
                if field.default is not None:
                    v = field.default
                elif field.default_factory is not None:
                    v = field.default_factory()
        else:
            types = self.fieldTypes(fieldName)
            if len(types) > 0:
                T = types[0]
                v = T()
        return v


class TypeInspection_dataclass(TypeInspection):
    def __init__(self, T):
        super().__init__(T)
        pass

    def allFieldNames(self) -> list[str]:
        v = []
        if self.T is None:
            pass
        else:
            v = list(self.T.__dataclass_fields__.keys())
        return v

    def fieldTypes(self, fieldName: str) -> list[Type]:
        v = []
        if self.T is None:
            pass
        else:
            field = self.T.model_fields.get(fieldName)
            if field is not None:
                v = get_args(field.annotation)
        return v

    def fieldHasDefault(self, fieldName: str) -> bool:
        v = False
        if self.T is None:
            pass
        else:
            field = self.T.__dataclass_fields__.get(fieldName)
            if field is not None:
                v = field.default is not None or field.default_factory is not None
        return v

    def fieldDefaultValue(self, fieldName: str) -> typing.Any:
        v = None
        if self.T is None:
            pass
        elif self.fieldHasDefault(fieldName):
            field = self.T.__dataclass_fields__.get(fieldName)
            if field is not None:
                if field.default is not None:
                    v = field.default
                elif field.default_factory is not None:
                    v = field.default_factory()
        else:
            types = self.fieldTypes(fieldName)
            if len(types) > 0:
                T = types[0]
                v = T()
        return v

#----------------------------------------------------------------------------

def isBaseModel(obj):
    log.info(f'isSqlModel: {dir(obj)}')
    return issubclass(obj, BaseModel)

def isDataclass(obj):
    log.info(f'isDataclass: {dir(obj)}')
    return hasattr(obj, '__dataclass_fields__')

def getTypeInspection(obj) -> TypeInspection:
    if isBaseModel(obj):
        return TypeInspection_BaseModel(obj)
    elif isDataclass(obj):
        return TypeInspection_dataclass(obj)
    else:
        return TypeInspection(obj)
