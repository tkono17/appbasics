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

def asTyped(value):
    t = type(value)
    x = value
    if t is str:
        lvalue = value.lower()
        if lvalue == 'true':
            x = True
        elif lvalue == 'false':
            x = False
        else:
            try:
                x = int(value)
            except ValueError:
                try:
                    x = float(value)
                except ValueError:
                    x = value
    return x
