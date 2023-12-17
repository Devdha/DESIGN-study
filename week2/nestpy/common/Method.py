def Method(method: str, path: str = ""):
    def decorator(func):
        func.__http_method = method
        func.__path = f"/{path.strip('/')}"
        return func
    return decorator

def Get(path: str = ""):
    def decorator(func):
        return Method("GET", path)(func)
    return decorator

def Post(path: str = ""):
    def decorator(func):
        return Method("POST", path)(func)
    return decorator