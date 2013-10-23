from storytracker.engine.interactibles import Interactible
from storytracker.engine.groups import Group
from storytracker.engine.helpers import React

class Human(Interactible):
    def __init__(self):
        self.state('alive')
        return super(Human, self).__init__()
    react=React()
    @react.to
    def kill(self, actor):
        if self.ability < actor.ability:
            self.ability -=1
            return 'attack'
        return 'die'

    def attack(self, target):
        target.kill


Tom = Human()
Steve=Human()
Tom.attack(Steve)
# Tom raises Event attack
# Steve gets Event, Tom is a kwarg