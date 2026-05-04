#!/usr/bin/env python3

from dataclasses import dataclass, fields
from typing import get_args, get_origin, Optional, get_type_hints

@dataclass
class User:
    id: int
    name: Optional[str]
    tags: list[str]
    value1: list[int|str] | None
    value2: list[int] | list[str] | float

# fields() で dataclass のフィールド情報を取得
for field in fields(User):
    # field.type が型アノテーション
    origin = get_origin(field.type)
    args = get_args(field.type)
    print(f"Field: {field.name}, Origin: {origin}, Type: {field.type}, Args: {args}")
    #print(f'field = {field}')

print('\n')
print(f'User = {get_type_hints(User, include_extras=True)}')
