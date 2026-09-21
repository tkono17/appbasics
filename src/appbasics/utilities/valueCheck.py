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
    types = [ int, float, bool, complex, str ]
    for T in types:
        value = tryTyped(svalue, T)
        if value is not None:
            break
    return value
