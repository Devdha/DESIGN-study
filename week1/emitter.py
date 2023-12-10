import asyncio

class Emitter:
    def __init__(self):
        self.events = dict()

    def __add(self, event, listener, once, filter=lambda _: True):
        if event not in self.events:
            self.events[event] = dict()

        self.events[event][listener.__name__] = {
            'listener': listener,
            'filter': filter,
            'once': once
        }

    def addListener(self, event, listener, filter=lambda _: True):
        self.__add(event, listener, False, filter)

    def on(self, event, filter):
        def decorator(func):
            self.__add(event, func, False, filter)

        return decorator

    def once(self, func, event, filter=lambda _: True):
        self.__add(event, func, True, filter)

    def removeListener(self, event, listener):
        if event not in self.events:
            return
        if listener not in self.events[event]:
            return
        del self.events[event][listener]

    def removeAllListeners(self, event):
        if event not in self.events:
            return
        del self.events[event]

    def emit(self, event, **kwargs):
        listeners = self.events[event]
        for k in listeners:
            filter_function = listeners[k]['filter']
            
            if filter_function is None or (filter_function(kwargs)):
                listener = listeners[k]['listener']

                if (asyncio.iscoroutinefunction(listener)):
                    asyncio.run(listener(kwargs))
                else:
                    listener(kwargs)

                
                if listeners[k]['once']:
                    self.removeListener(event, k)
