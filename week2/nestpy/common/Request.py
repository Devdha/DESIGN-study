from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class Body(BaseModel, Generic[T]):
    def __init__(self, cls: T) -> None:
        self.cls = cls

    def __get__(self, instance, owner):
        return self.cls(instance.request.json)
    
    def __set__(self, instance, value):
        instance.request.json = value
    
class Query(BaseModel, Generic[T]):
    def __init__(self, cls: T) -> None:
        self.cls = cls

    def __get__(self, instance, owner):
        return self.cls(instance.request.args.get(self.name))
    
    def __set__(self, instance, value):
        instance.request.args[self.name] = value
    
class Param(BaseModel, Generic[T]):
    def __init__(self, cls: T) -> None:
        self.cls = cls

    def __get__(self, instance, owner):
        return self.cls(instance.request.view_args.get(self.name))
    
    def __set__(self, instance, value):
        instance.request.view_args[self.name] = value