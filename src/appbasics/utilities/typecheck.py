from dataclasses import fields
from typing import get_args


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
