import pytest
from storytracker.engine.helper import Handler, Event, EventError
from storytracker.tests import callback

destruction=Event()
def func(**kwargs):
    return True

class Room(object):
    handlers=set()
    destruction=destruction

room=Room()

# should be handled, even if return Value is False:
def hand(**kwargs):
    return False
handle_dest=Handler(hand,req=[destruction])

@handle_dest
def argh(**kwargs):
    print "AAAAAH!"

def test_hand():
    with pytest.raises(EventError):
        room.destruction()
    room.destruction(func)
    assert room.destruction.instance == room
    # Testing if False-handler gets handled:
    assert handle_dest.handle(destruction)==hand()==False
    
    # giving the handler a function to call:
    @handle_dest
    @callback(this='that')
    def screaming(**kwargs):
        print 'AAAAARGH!'
    handle_dest.handle(room.destruction, this='that')
    t=room.destruction
    handle_dest.handle(t(this='that'))