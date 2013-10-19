
import inspect

def react(func):
    func.act=False
    return func

def act(func):
    func.act=True
    return func

class Handler(object):
    handlers={}
    def __new__(cls, handler, event=None):
        if event:
            if event.name in cls.handlers:
                cls.handlers[event.name].append(handler)
            else:
                cls.handlers[event.name]=[handler]
        return cls.__init__(handler)

    def __init__(self, handler):
        self.handler = handler

    def __set__(self, event):
        handlers[event.name].append(self.handler)
        event.handlers.append(self)

    def handle(self, event):
        if event == self.event:
            return self.handler(event)

class Event(object):
    def __init__(self, event):
        self.handlers=[]
        if callable(event):
            name=event.__name__
        else:
            name=event
            def ev(**kwargs):
                return event
            event=ev

        self.event=event
        self.name=name

    def __call__(self, func=None, **kwargs):
        if callable(func):
            self.event=func
        else:
            for hand in self.handlers:
                if hand(self)=="catch":
                    break
            return True