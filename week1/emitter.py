import asyncio

class EventEmitter:
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

    def once(self, event, func, filter=lambda _: True):
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

    async def __emit(self, event, **kwargs):
        if event not in self.events:
            print("Event not found")
            return
        listeners = self.events[event]
        asyncTasks = []
        syncTasks = []
        onceTasks = []
        for k in listeners:
            filter_function = listeners[k]['filter']
            if filter_function is None or (filter_function(kwargs)):
                listener = listeners[k]['listener']

                if (asyncio.iscoroutinefunction(listener)):
                    asyncTasks.append(listener)
                else:
                    syncTasks.append(listener)

                if listeners[k]['once']:
                    onceTasks.append(k)
    

        [task(kwargs) if task.__code__.co_argcount else task() for task in syncTasks]
        await asyncio.gather(*[task(kwargs) if task.__code__.co_argcount else task() for task in asyncTasks])
        [self.removeListener(event, listener) for listener in onceTasks]
                
    def emit(self, event, **kwargs):
        asyncio.run(self.__emit(event, **kwargs))
        
