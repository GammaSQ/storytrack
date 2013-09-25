
def callback(*args, **kwargs):
    if 'ret' in kwargs:
        ret=kwargs['ret']
        del kwargs['ret']
    else:
        ret=None

    if 'callback' in kwargs:
        callback = kwargs['callback']
        del kwargs['callback']
    else:
        callback = None

    def testing(*testargs, **testkwargs):
        assert(len(args)==len(testargs))
        for i, n in enumerate(args):
            if n != None:
                assert(testargs[i]==n)

        assert(len(kwargs)<=len(testkwargs))
        for key, val in kwargs:
            assert(key in testkwargs)
            if val != None:
                assert(testkwargs[key]==val)

        if not callback:
            return ret

        if ret != None:
            assert(ret == callback(*args, **kwargs))
            return ret

        return callback(*args, **kwargs)

    return testing
