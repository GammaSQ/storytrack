import pytest

from storytracker.tests import callback

from storytracker.engine import storyline
from storytracker.engine.interactables import Interactable

a = storyline()#timesteps=real/played/own

Mitch=Interactable()
a.Mitch=Mitch

class TestStoryline:

    def test_basic_reg(self):
        assert a.Mitch==Mitch
        assert a.Mitch.name == "Mitch"