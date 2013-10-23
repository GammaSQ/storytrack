from storytracker.engine.groups import Group
from storytracker.engine.interactables import Interactable

class Room(Group):
    pass

class Pax(object):
    def __init__(self, *args):
        self.handler=set(args)

    def handlers(self, base=None):
        if base != None:
            ret = base & self.handler
            assert len(ret) == len(self.handler)
            return ret
        return self.handler

room=Room()

k = [Pax(i, i+1) for i in range(5)]
# Test basic properties:
room.join(k[0])
assert room.handlers() == set(range(2))
room.members=set(k)
assert room.handlers() == set(range(6))
room.leave(k[-1])
assert room.handlers() == set(range(5))
room.leave(k[2])
assert room.handlers() == set(range(5))

# -------------------------------------------------

from storytracker.engine.helper import Handler, Event
from storytracker.tests import callback

Room.collapse = Event('collapse')
flee = Handler(True, req=[Room.collapse])
@flee
def run(hint, **kwargs):
    return "RUUAAAAANN!!!"


A=Room()
B=Room()

k=[]
for i in range(9):
    flee = Handler(True, req=[Room.collapse])
    Room.collapse.register(flee)
    @flee
    @callback(True)
    def run(hint, **kwargs):
        return "RUUAAAAANN!!!"
    k.append(Pax(flee))

flee=Handler(True, req=[Room.collapse])
Room.collapse.register(flee)
@flee
def run(hint, **kwargs):
    assert False

p = Pax(flee)

for i in k[:4]:
    A.join(i)

for i in k[4:]:
    B.join(i)
# Nothing should happen, except for screams
A.collapse()
B.collapse()

B.join(p)

#Again, nothing should happen:
A.collapse()

#And THIS should raise the assertion-Error:
import pytest
with pytest.raises(AssertionError):
    B.collapse()