from pydantic import BaseModel

class NestApplication(BaseModel):
    module = None
    __instance = None

    def __init__(self, module):
        self.module = module

    @classmethod
    def __getInstance(cls):
        return cls.__instance
    
    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        
        cls.instance = cls.__getInstance
        return cls.__instance
    
    def serve():
        pass


class NestFactory(BaseModel):
    @classmethod
    def create(cls, module):
        return NestApplication(module)