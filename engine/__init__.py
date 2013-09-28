from storycheck.engine.interactables import interactible
import inspect

class storyline(object):
    #self.map=[]
    def __init__(self, prev_chap=None):
        if prev_chap and type(prev_chap) == storyline:
            self.connections=prev_chap.connectins
            self.interactibles=prev_chap.interactibles
            self.knownledge=prev_chap.knownledge

    def __setattr__(self, attr, ret):
        if issubclass(type(ret), interactible):
            ret.name=attr
        elif attr.startswith("__"):
            pass
        else:
            ret=interactible(ret)
            ret.name=attr
        return super(storyline, self).__setattr__(attr, ret)

    def register_interactibles(self, interactibles):
        for i in interactibles:
            if i in self.interactibles:
                raise ArgumentError("This interactible already exists!")

class fit_args_and_kwargs_to_call(object):
    def __init__(self, needed_args=[]):
        self.unpassed_args=[]
        self.unpassed_kwargs={}
        if callable(needed_args):
            self.neded_args=[]
            return self.__call__(needed_args)
        self.needed_args=needed_args

    def __call__(call):
        arg_kwarg=inspect.getargspec(call)
        pre_args=arg_kwarg[0] or []
        varargs = bool(arg_kwarg[1])
        varkwargs=bool(arg_kwarg[2])
        pre_kwargs=list(arg_kwargs[3]) if arg_kwargs[3] else []

        missing=[]
        for n in needed_args:
            if n not in args:
                missing.append(n)
        if missing:
            raise TypeError("%s has to get %s as arguments!"%(call.__name__, ', '.join(missing)))

        pre_kwargs={}
        for val in pre_kwargs.reverse():
            kw=args.pop()
            kwargs[kw]=val
        defargs=pre_args
        defkwargs=pre_kwargs.keys()
        
        def nested(*args, **kwargs):
            jump=[]
            pass_args=[]
            pass_kwargs={}
            for n in defargs:
                if n in kwargs:
                    jump.append(n)
            jump = jump
            args.reverse()
            for defarg in defargs:
                if defarg == jump[-1]:
                    tmp = jump.pop()
                    pass_args.append(kwargs[tmp])
                    del kwargs[tmp]
                else:
                    pass_args.append(args.pop())
            args.reverse()

            if len(pass_args)<len(defargs):
                raise TypeError("%s takes at least %i non-kw - arguments. %i defined." %(call.__name__, len(defargs), len(pass_args)))
            
            self.unpassed_args=args
            self.unpassed_kwargs=kwargs

            pass_args += args if varargs else []
            pass_kwargs += kwargs if varkwargs else {}
            defargs=pre_args
            defkwargs=pre_kwargs.keys()
            #for n in needed_pass_args:
            #    if n not in 
            return call(*pass_args, **pass_kwargs)
        return nested

    def last_unpassed(self, kwargs=False):
        if kwargs:
            return self.unpassed_kwargs

        return self.unpassed_args

    def last_unpassed_args(self):
        return self.unpassed_args

    def las_unpassed_kwargs(self):
        return self.unpassed_kwargs
