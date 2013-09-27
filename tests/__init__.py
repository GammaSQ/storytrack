
def callback(*args, **kwargs):
    if 'ret' in kwargs:
        ret=kwargs['ret']
        del kwargs['ret']
    else:
        ret=None

    def default():
        return ret

    def wrapper(func=default):
        def testing(*testargs, **testkwargs):
            assert(len(args)==len(testargs))
            for i, n in enumerate(args):
                if type(n)==type:
                    assert(type(testargs[i])==n)
                elif n != None:
                    assert(testargs[i]==n)

            assert(len(kwargs)<=len(testkwargs))
            for key, val in kwargs.iteritems():
                assert(key in testkwargs)
                if type(val) == type:
                    asset((testkwargs[key])==val)
                elif val != None:
                    assert(testkwargs[key]==val)

            if func==default:
                return ret

            if ret != None:
                assert(ret == func(*testargs, **testkwargs))
                return ret

            return func(*testargs, **kwargs)

        return testing

    return wrapper
