from pydantic import BaseModel
from typing import Any, ClassVar
import http.server

import json
from nestpy.common import registered_controllers
from nestpy.core import HTTPRequestStrategy, GetStrategy, PostStrategy

import urllib.parse

def serialize_to_json(data):
    if isinstance(data, list):
        res = [item.dict() for item in data]
        return json.dumps(res)
    if isinstance(data, dict):
        return json.dumps(data)
    if isinstance(data, BaseModel):
        return data.model_dump_json()
    if hasattr(data, 'to_dict'):
        return json.dumps(data.to_dict())
    return json.dumps(data)

class NestApplicationRequestHandler(http.server.BaseHTTPRequestHandler):
    def set_strategy(self, strategy: HTTPRequestStrategy):
        self.strategy = strategy

    def map_path_to_method(self, method: str) -> Any:
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        for controller_path, controller in registered_controllers.items():
            if path.startswith(controller_path):
                attr_list = dir(controller)
                for attr in attr_list:
                    method_func = getattr(controller, attr)
                    if hasattr(method_func, '_http_method') and hasattr(method_func, '_path'):
                        print(path, method_func._http_method, method_func._path, f"{controller_path}/{method_func._path}")
                        method_path = f"{controller_path}" + f"/{method_func._path}" if method_func._path != '' else f"{controller_path}"
                        if method_func._http_method == method and path == method_path:
                            return method_func
                        
    def handle_method(self, method: Any):
        return

        
                        
    def get_body(self):
        content_length = self.headers['Content-Length']
        if (content_length is None):
            return {}
        body = self.rfile.read(int(content_length))
        return json.loads(body)
    
    def get_query_params(self):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        return query
    
    def get_path_params(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        if path == '/':
            return {}
        
        params = path.strip('/').split(' ')
        param_dict = {}
        for param in params:
            if param != '':
                key, value = param.split('=')
                param_dict[key] = value

        return path


    def do_GET(self):
        self.set_strategy(GetStrategy())
        self.strategy.process_request(self)

    def do_POST(self):
        self.set_strategy(PostStrategy())
        self.strategy.process_request(self)

# NOTE - Singleton Pattern
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


# NOTE - Factory Pattern
class NestFactory(BaseModel):
    @classmethod
    def create(cls, module):
        return NestApplication.instance(module)