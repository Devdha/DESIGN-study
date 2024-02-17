from typing import Any

def Injectable():
    def wrap(cls: Any) -> Any:
        cls._is_injectable = True
        return cls
  
    return wrap