from pydantic import Dict, Any

def Module(module_config: Dict[str, Any]) -> Any:


    def wrap(cls: Any) -> Any:
        cls.__module_config = module_config
        return cls

    return wrap