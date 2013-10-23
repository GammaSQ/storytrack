import inspect

class React(object):
    def __init__(self):
        self.boring_handlers={}
        self.handler_args=set()

    def to(self, func):
        self.boring_handlers[func.__name__]=func

    def ion(self, *args):
        def wrapper(func):
            assert callable(func)
            self.handler_args.add((func, args))
            return func
        return wrapper

class Act(object):
    def __init__(self):
        self.boring_handlers={}
        self.handlers=set()

    def ing(self, func):
        pass

def react(func):
    func.act=False
    return func

def act(func):
    func.act=True
    return func

class Handler(object):
    def __init__(self, handler, reg=[], req=[], conflicts=[], standalone=True):
        if not callable(handler):
            def hand(**kwargs):
                return handler
            self.handler=hand
        else:
            self.handler=handler
        for ev in reg:
            ev.register(self)
        self.req=set(reg) | set(req)
        self.conflicts=conflicts
        self.standalone=standalone

    def __call__(self, func):
        if not callable(func):
            def tmp(**kwargs):
                return func
            self.func=tmp
            return self
        else:
            self.func=func
        return func

    def handle(self, event, **kwargs):
        if event not in self.req:
            return None
        for ev in self.req:
            if not (ev==event or ev.present()):
                return None
        for ev in self.conflicts:
            if ev.present():
                return None
        hand = self.handler(**kwargs)
        if self.standalone and hand:
            ####### What to do with return Value????
            self.func(hand, **kwargs)
        return hand

    def __get__(self, instance, cls=None):
        self.instance=instance
        self.cls=cls
        return self

    def set_instance(self):
        tmp = self.handler
        def dummy(**kwargs):
            return tmp(self.instance, **kwargs)
        self.handler = dummy

    def reg_req(self, req):
        if type(req) == list:
            self.req += req
        elif type(req) == Event:
            self.req.append(req)
        else:
            raise TypeError("Only events can be required for action!")

    def drop_req(self, req):
        if not type(req)==Event:
            raise TypeError("Only events can be required for action!")
        try:
            i=self.req.index(req)
        except ValueError:
            return None
        self.req.pop(i)

    def reg_conflicts(self, conflicts):
        if type(conflicts) == list:
            self.conflicts += conflicts
        elif type(conflicts) == Event:
            self.conflicts.append(conflicts)
        else:
            raise TypeError("Only events can be conflictsuired for action!")

    def drop_conflict(self, conflict):
        if not type(conflict)==Event:
            raise TypeError("Only events can be conflictsuired for action!")
        try:
            i=self.conflicts.index(conflict)
        except ValueError:
            return None
        self.conflicts.pop(i)

class Event(object):
    def __init__(self, event=None):
        if event != None and not callable(event):
            def ev(**kwargs):
                return event
            event=ev

        self.event=event
        self.handlers=set()
        self.called = False
        self.instance=None

    def __get__(self, instance, cls=None):
        self.instance=instance
        self.cls = cls
        return self

    def register(self, handler):
        self.handlers.add(handler)
    
    def drop(self, handler):
        self.handlers.discard(handler)

    def __call__(self, func=None, **kwargs):
        if func != None:
            if not callable(func):
                def ev(**kwargs):
                    return func
                func=ev
            self.event=func
        else:
            if self.called:
                return kwargs
            try:
                run= self.event(**kwargs)
            except TypeError:
                err = EventError("No event specified!")
                raise err()
            ext_hand=self.instance.handlers
            if callable(ext_hand):
                ext_handlers=self.handlers & ext_hand(self.handlers)
            else:
                ext_handlers=self.handlers & ext_hand
            for handler in ext_handlers:
                hand = handler.handle(self, **kwargs)
                if hand== "catch":
                    break
            #except AttributeError:
            #    raise EventError("Event not called as classmember!")
class EventError(Exception):
    def __init__(self, message):
        self.m = message
    def __call__(self):
        print self.m
        return self