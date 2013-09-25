from __future__ import with_statement

import pytest

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

from storycheck.menue import menue

class TestCallback:
    def bad_example(*args, **kwargs):
        assert(len(args)==5)
        assert(len(kwargs)==4)
        return 4

    def __init__(self):
        self.testcall1=callback(*range(5), This="that", There="Then", Blah=None, ret=4)
        self.testcall2=callback(*range(5), This="that", There="Then", Blah=None)
        self.testcall3=callback(This="that", There="Then", Blah=None, ret=4, callback=bad_example)
        self.testcall4=callback()

    def test_pos(self):
        ret=self.testcall1(0,1,2,3,4,This="that", There="Then", Blah="Meh", Extra="null")
        assert(ret==4)
        ret=self.testcall2(0,1,2,3,4,This="that", There="Then", Blah="Meh", Extra="null")
        assert(ret==None)
        ret=self.testcall3(This="that", There="Then", Blah="Meh", Extra="null")
        assert(ret==4)
        ret=self.testcall4()
        assert(ret==None)


    def test_neg(self):
        with pytest.raises(AssertionError):
            self.testcall1(0,1,2,3,4)
        with pytest.raises(AssertionError):
            self.testcall1(0,1,2,3,4,This="that", There="Then", Extra="null")
        with pytest.raises(AssertionError):
            self.testcall1()

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
