from ..typecheck import getTypeInspection

def entryCreate(TCreate):
    entry = None
    if T is None:
        return entry
    else:
        tcheck = getTypeInspection(TCreate)
        entry = tcheck.dataCreate()
    return entry

def entryUpdate(TUpdate):
    entry = None
    if TUpdate is None:
        return entry
    else:
        tcheck = getTypeInspection(TUpdate)
        entry = tcheck.dataUpdate()
    return entry

