from __future__ import with_statement

import pytest

class callback:
    def __init__(self, *args, **kwargs):
        if 'ret' in kwargs:
            self.ret=kwargs['ret']
            del kwargs['ret']
        else:
            self.ret=None

        if 'callback' in kwargs:
            self.callback = kwargs['callback']
            del kwargs['callback']
        else:
            self.callback = None

        self.args=args
        self.kwargs=kwargs

    def __call__(self, *args, **kwargs):
        assert(len(args)==len(self.args))
        for i, n in enumerate(self.args):
            assert(args[i]==n)

        assert(len(kwargs)>=len(self.kwargs))
        for key, val in self.kwargs:
            assert(key in kwargs and kwargs[key]==val)

        if not self.callback:
            return self.ret

        if self.ret:
            assert(self.ret == self.callback(*args, **kwargs))
            return self.ret

        return self.callback(*args, **kwargs)

from storycheck.menue import menue

class TestMenue:
    options=[callback(ret=k) for k in range(5)]
    kw_options={}
    for k in range(5):
        kw_options['THIS IS %i'%k] =callback(ret=k)
    
    def test_question_positive(self):
        pending = menue(self.options, callback(ret=2))
        assert(pending()==2)
        for j in range(5):
            assert(pending(j)==j)

    def test_questions_negative(self):
        pending = menue(self.options, callback(ret = 2))
        assert(pending(arg=213, kljssaf=29)==2)
        assert(pending(2)==2)
        with pytest.raises(IndexError):
            pending(30)
        pending = menue(self.options, callback(ret = "Not an Int"))
        with pytest.raises(TypeError):
            pending(arg=None)
        with pytest.raises(TypeError):
            pending(None)

    def test_question_kw_positive(self):
        pending=menue(self.kw_options, callback(ret="THIS IS 2"))
        assert(pending()==2)
        assert(pending("THIS IS 3")==3)
        with pytest.raises(KeyError):
            pending("This is not a key!")
        with pytest.raises(KeyError):
            pending=menue(self.kw_options, callback(ret="This is no key either"))
            pending()
        with pytest.raises(KeyError):
            pending(4)
