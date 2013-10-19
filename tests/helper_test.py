import pytest
from storytracker.engine.helper import hyper_call

basics=hyper_call('here')

@basics
def a_callable(here, there, this='that', foo='bar'):
    pass

@basics
def certain_test(fist, here="There"):
    pass

@basics
def a_varargs_callable(here, there, *args, **kwargs):
    pass

@basics
def a_testing_callable(here, there, *args, **kwargs):
    assert here=="there"
    assert there==1
    assert list(args) == range(4)

def a_simple_test(here):
    pass

a_simple_test = basics(a_simple_test)


def test_basic_usage_pos():
    certain_test(1, 2)
    a_callable(1, 2, 3, 4, 5, 6, 7, 8)
    assert(basics.last_unpassed_args() == [5, 6, 7, 8])
    a_callable(2, foo='me', this='bonk', here='there', be="2be")
    assert(basics.last_unpassed_kwargs()==dict(be="2be"))

def test_advanced_usage_pos():
    a_varargs_callable(1,2,4,5, here="there")
    a_varargs_callable('test', 'teeest', 1,2,4,5,6)
    a_testing_callable(*[1]+range(4), here="there")

def test_basic_usage_neg():
    with pytest.raises(TypeError):
        # No args specified = TypeError
        a_callable()

    with pytest.raises(TypeError):
        # Second Argumend not specified = TypeError
        a_callable(here='there', this='there')

    with pytest.raises(TypeError):
        # needed_args not specified = TypeError
        @basics
        def an_illegal_callable():
            pass
    
    with pytest.raises(TypeError):
        # If an argument is not specified = TypeError
        a_varargs_callable(here='hm', balh='meh')
