from storytracker.engine.groups import Group
from storytracker.engine.interactables import Interactable
from storytracker.engine.helper import React, Event


class Room(Group):
    collapse = Event(True)

class Person(Interactable):
    react=React()

    def __init__(self, val=1):
        self.val=val
        return super(Person, self).__init__()

    def run(self):
        assert(self.val!=0)
        return "FAST!"

    @react.ion(Room.collapse)
    def react_to_collapse(self):
        return 'run'

A=Room()
B=Room()

Bill=Person()
Tim=Person()
Tom=Person()
Traitor=Person(0)

A.join(Bill)
A.join(Tim)
B.join(Tom)
assert len(A.members) == len(A.handlers())
A.collapse()
B.collapse()
B.join(Traitor)

import pytest
with pytest.raises(AssertionError):
    B.collapse()