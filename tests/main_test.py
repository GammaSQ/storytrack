from __future__ import with_statement

import pytest

from storycheck.tests import callback

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
