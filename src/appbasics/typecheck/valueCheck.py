from dataclasses import fields
from typing import get_args


def tryTyped(value, T):
    v = None
    try:
        v = T(value)
    except ValueError:
        v = None
    return v

def valueTyped(svalue):
    value = None
    # Check bool
    if svalue.lower() in ['true', '1', 'yes']:
        value = True
    elif svalue.lower() in ['false', '0', 'no']:
        value = False
    else:
        types = [ int, float, complex, str ]
        for T in types:
            tvalue = tryTyped(svalue, T)
            if tvalue is not None:
                value = tvalue
                break
    return value
