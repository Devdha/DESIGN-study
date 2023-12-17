from typing import Any

def Injectable():
    def wrap(cls: Any) -> Any:
        cls.__injectable = True
        return cls
  
    return wrap