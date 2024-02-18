def copy_annotations(from_func, to_func):
    to_func.__annotations__ = from_func.__annotations__

def Get(path=''):
    def wrapper(func):
        def wrapped_func(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        wrapped_func._http_method = 'GET'
        wrapped_func._path = path.strip('/')
        copy_annotations(func, wrapped_func)
        return wrapped_func
    return wrapper

def Post(path=''):
    def wrapper(func):
        def wrapped_func(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        wrapped_func._http_method = 'POST'
        wrapped_func._path = path.strip('/')
        copy_annotations(func, wrapped_func)
        return wrapped_func
    return wrapper