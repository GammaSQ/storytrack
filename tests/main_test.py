from __future__ import with_statement

import pytest

from storytracker.tests import callback

@callback(*range(5), This="that", There="Then", Blah=None, ret=4)
def bad_example(*args, **kwargs):
    assert(len(args)==5)
    assert(len(kwargs)==4)
    return 4

call1=callback(*range(5), This="that", There="Then", Blah=None, ret=4)()
call2=bad_example
call3=callback(This="that", There="Then", Blah=None)()
call4=callback()()

class TestCallback(object):

    def test_pos(self):
        ret=call1(0,1,2,3,4,This="that", There="Then", Blah="Meh", Extra="null")
        assert(ret==4)
        ret=call2(0,1,2,3,4,This="that", There="Then", Blah="Meh", Extra="null")
        assert(ret==4)
        ret=call3(This="that", There="Then", Blah="Meh", Extra="null")
        assert(ret==None)
        ret=call4()
        assert(ret==None)


    def test_neg(self):
        with pytest.raises(AssertionError):
            call1(0,1,2,3,4)
        with pytest.raises(AssertionError):
            call1(0,1,2,3,4,This="that", There="Then", Extra="null")
        with pytest.raises(AssertionError):
            call1()

