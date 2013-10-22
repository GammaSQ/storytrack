from __future__ import with_statement
from storytracker.tests import callback
from storytracker.engine.interactables import Interactable
from storytracker.engine.helper import act, react
import pytest

def scream(actor,*args):
    for n in args:
        print n

class ball(Interactable):
    def __init__(self, thrower):
        super(ball, self).__init__()
        self.thrower=thrower
        self.state('held')

    @act
    def throw(self, target=None):
        self.state("flying")

    @react
    def hit(self, actor, mod=None):
        if self.state('flying'):
            self.state('hit', 50)
        else:
            self.state('hit', 0)

class batter(Interactable):
    def __init__(self, hated=[]):
        self.hated=hated
        super(batter, self).__init__()

    @react
    @callback(None, ball)
    def throw(self, ball):
        if ball.thrower in self.hated:
            return 'hit', dict(chance=100, target=ball)
        return 'hit', dict(chance=60, target=ball)

    @act
    def hit(self, ball, chance):
        if chance > 70:
            return {}
        else:
            scream(self, "ARGH!")
            return dict(mod=20)

#reaction = callback(batter, ball, callback=to_be_called)

#batter.react_to_throw = reaction

batter1=batter()
batter2=batter(["Bill", "Berg"])
batter3=batter(["Achim", "Thomas"])
ball1=ball("Nobody")
ball2=ball("Bill")
ball3=ball("Thomas")

class TestInteractable_via_batter:

    def test_state_pos(self):
        assert(ball1.state('held')==True)
        batter1.state("This", "that")
        assert(batter1.state("This")=="that")
        batter1.state("This", None)
        assert(batter1.read_state("This")==None)
        assert(batter1.state("This")==None)
        assert(batter1.state("This")==True)

    def test_state_neg(self):
        batter1.state("This", "tall")

        with pytest.raises(TypeError):
            batter1.state("This", "call", value="There")
        assert(batter1.read_state("This")=="tall")

        with pytest.raises(TypeError):
            batter1.state("Hm", "call", key="This")
        assert(batter1.read_state("Hm")==None)

        with pytest.raises(TypeError):
            batter1.state("Hm", key="This")
        assert(batter1.read_state("Hm")==None)

    def test_reaction_pos(self):
        ball1.act_on('throw', target=batter1)
        assert ball1.state('flying')
        assert ball1.read_state('hit') == 50