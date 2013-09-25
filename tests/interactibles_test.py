from tests import callback
from storycheck.engine.interactibles import interactible

def scream(actor,*args):
    if getattr(actor, 'talk', None) and (not getattr(actor, 'can_not_scream', None) or getattr(actor, 'scream', None)):
        for n in args:
            print n

def flying_ball(actor, mod=None):
    pass

class batter(interactible):
    def __init__(self, hated=[]):
        self.hated=hated

    def react_to_flying_ball(self, ball):
        if ball.thrower in self.hated:
            return 'hit', 100
        return 'hit', 60

    def hit(self, chance):
        if chance > 70:
            return flying_ball(self)
        else:
            scream(self, "ARGH!")
            return flying_ball(self, -20)

class ball(interactible):
    self.state='held'
    def __init__(self):