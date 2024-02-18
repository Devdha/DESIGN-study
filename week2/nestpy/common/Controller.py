from typing import Any, Dict
from .Module import registered_controllers

def Controller(path: str = '/', controller_config: Dict[str, Any] = []) -> Any:
    # NOTE - all wrapper functions are decorator patterns
    def wrap(cls: Any) -> Any:
        cls.__path = '/'
        if path:
            cls.__path = f"/{path.strip('/')}"
        cls.__controller_config = controller_config

        registered_controllers[path] = cls

        return cls

    return wrap