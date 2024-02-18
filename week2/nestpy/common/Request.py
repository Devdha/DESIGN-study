from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class RequestParam(Generic[T]):
    def __init__(self, data: T):
        self.data = data

class Body(RequestParam[T]):
    pass

class Query(RequestParam[T]):
    pass

class Param(RequestParam[T]):
    pass