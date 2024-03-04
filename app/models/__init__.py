from enum import Enum
from typing import Any

import pydantic


class CRUDActionEnum(str, Enum):
    create = 'create'
    update = 'update'
    delete = 'delete'


class AnyJson(pydantic.RootModel[Any]):
    """Root Model to accept any payload"""
    root: Any
