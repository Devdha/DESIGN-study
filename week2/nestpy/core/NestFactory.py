from pydantic import BaseModel
from typing import Any, get_origin, get_args, Union
import http.server

import json
from nestpy.common import registered_controllers, Body, Query, Param
from nestpy.core import HTTPRequestStrategy, GetStrategy, PostStrategy

import urllib.parse

class NestApplicationRequestHandler(http.server.BaseHTTPRequestHandler):
    def set_strategy(self, strategy: HTTPRequestStrategy):
        self.strategy = strategy

    def map_path_to_method(self, method: str) -> Any:
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path.strip('/')

        for controller_path, controller in registered_controllers.items():
            controller_path = controller_path
            if path.startswith(controller_path):
                attr_list = dir(controller)
                for attr in attr_list:
                    method_func = getattr(controller, attr)

                    if hasattr(method_func, '_http_method') and hasattr(method_func, '_path'):
                        if controller_path.split('/')[-1] == '':
                            method_path = (controller_path + method_func._path.lstrip('/')).rstrip('/')
                        else:
                            method_path = (controller_path.rstrip('/') + '/' + method_func._path.lstrip('/')).rstrip('/')

                        if method_func._http_method == method and path == method_path:
                            return method_func
                        
                        if method_func._http_method == method and ':' in method_func._path:
                            path_parts = path.split('/')
                            method_parts = method_path.split('/')
                            if path_parts[0] == '':
                                continue
                            if len(path_parts) == len(method_parts):
                                for i in range(len(method_parts)):
                                    if method_parts[i] != path_parts[i] and ':' in method_parts[i]:
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
        path = parsed_path.path.strip('/')
        if path == '':
            return ''
        
        return path
    
    def is_of_type(self, hint, of_type):
        if hint == of_type:
            return True
        
        origin = get_origin(hint)
        args = get_args(hint)
        
        return origin == of_type or any(arg == of_type or get_origin(arg) == of_type for arg in args if arg is not type(None))
    
    def is_optional_of_type(self, hint, of_type):
        origin = get_origin(hint)
        if origin is not Union:
            return False
        
        args = get_args(hint)
    
        if type(None) not in args:
            return False
        
        return any(arg == of_type or get_origin(arg) == of_type for arg in args if arg is not type(None))

    
    def map_inputs(self, method, body, query, path):
        annotations = method.__annotations__
        inputs = {}

        for param, annotation in annotations.items():
            if param == 'return':
                continue

            if self.is_of_type(annotation, Body):
                if body is None:
                    raise Exception('Body is required')

                cls = get_args(annotation)[0]
                inputs[param] = Body(data=cls(**body))

            elif self.is_of_type(annotation, Query):
                value = query.get(param)
                if value is None:
                    if not self.is_optional_of_type(annotation, Query):
                        raise Exception(f'Query parameter {param} is required')
                    continue
                inputs[param] = Query(data=value[0])
            elif self.is_of_type(annotation, Param):
                value = path
                if value is None:
                    if not self.is_optional_of_type(annotation, Query):
                        raise Exception(f'Path parameter {param} is required')
                    continue
                inputs[param] = Param(data=value)
            
        return inputs


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