from dataclasses import fields
from typing import get_args

class ValueCheck:
    def __init__(self):
        pass

    def type(self):
        t = None
        return t
    
    def toStr(self, value):
        return str(value)
    
    def fromStr(self, svalue):
        value = None
        t = self.type()
        match value:
            case None:
                value = ''
            case str():
                value = svalue
            case int():
                value = int(svalue)
            case float():
                value = float(svalue)
            case _:
                value = svalue
        return value
    
class TypeCheck:
    def __init__(self, valueType):
        self.type = valueType
        pass

    def defaultValue(self):
        x = None
        return None
    
    def subTypes(self):
        v = []
        return v
    
class FieldCheck:
    def __init__(self, fieldType):
        self.fieldType = fieldType
        pass

    def possibleTypes(self):
        v = []
        if self.fieldType is None:
            pass
        else:
            v = get_args(self.fieldType)
        return v

    def defaultValue(self):
        x = None
        return None
    
    def subTypes(self):
        v = []
        return v
    