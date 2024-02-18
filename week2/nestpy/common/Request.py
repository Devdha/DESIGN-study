from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class Body(Generic[T]):
    def __init__(self, type_: TypeVar = None):
        self.type = type_

class Query(Generic[T]):
    def __init__(self, type_: TypeVar = None):
        self.type = type_

class Param(Generic[T]):
    def __init__(self, type_: TypeVar = None):
        self.type = type_