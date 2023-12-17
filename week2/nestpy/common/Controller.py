from typing import Any, Dict, Optional

def Controller(path: str = '/', controller_config: Dict[str, Any] = []) -> Any:
    def wrap(cls: Any) -> Any:
        cls.__path = '/'
        if path:
            cls.__path = f"/{path.strip('/')}"
        cls.__controller_config = controller_config
        return cls

    return wrap