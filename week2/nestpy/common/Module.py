from typing import Dict, Any

registered_controllers = {}
registered_services = {}

def Module(module_config: Dict[str, Any]) -> Any:
    def wrap(cls: Any) -> Any:
        cls.__module_config = module_config

        service = module_config.get('provider')
        if service:
            try:
                if service._is_injectable is True:
                    registered_services[service.__name__] = service
                else:
                    raise Exception('Service is not defined')
            except AttributeError:
                raise Exception(f"There's no injectable service named {service.__name__}")
        
        controller = module_config.get('controller')
        if controller:
            registered_controllers[controller.__path] = controller
        else:
            raise Exception('Controller is not defined')
        
        providers = {}
        for name, type in controller.__init__.__annotations__.items():
            if type._is_injectable:
                provider = registered_services[type.__name__]
                if not provider:
                    raise Exception(f'Provider {name} is not defined')
                providers[name] = provider
        instance = controller(**providers)
        registered_controllers[controller.__path] = instance
        
        return cls

    return wrap