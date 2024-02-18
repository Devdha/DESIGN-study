from nestpy.common import Module, Controller
from nestpy.core import NestFactory

class TestService:
    pass

@Controller()
class TestController:
    def __init__ (self, service: TestService):
        pass

@Module({'controller': TestController})
class TestModule:
    pass

if __name__ == '__main__':
    app = NestFactory.create(TestModule)
    app.serve()
