from pydantic import BaseModel
from typing import Any, ClassVar
import http.server

class NestApplicationRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

class NestApplication():
    __instance = None
    module: Any

    def __init__(self, module: Any) -> None:
        self.module = module

    @classmethod
    def __getInstance(cls):
        return cls.__instance
    
    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        
        cls.instance = cls.__getInstance
        return cls.__instance
    
    def serve(self):
        address = 'localhost'
        port = 3001
        server_address = (address, port)

        httpd = http.server.HTTPServer(server_address, NestApplicationRequestHandler)
        print(f'Server is running on {address}:{port}')

        httpd.serve_forever()


class NestFactory(BaseModel):
    @classmethod
    def create(cls, module):
        return NestApplication.instance(module)