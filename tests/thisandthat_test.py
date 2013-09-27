import pytest

from storycheck.tests import callback

from storycheck.engine import storyline
from storycheck.engine.interactables import interactible

a = storyline()#timesteps=real/played/own

Mitch=interactible()
a.Mitch=Mitch

class TestStoryline:

    def test_basic_reg(self):
        assert a.Mitch==Mitch
        assert a.Mitch.name == "Mitch"