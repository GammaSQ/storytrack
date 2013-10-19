from storytracker.engine.interactables import interactable

class storyline(object):
    #self.map=[]
    def __init__(self, prev_chap=None):
        if prev_chap and type(prev_chap) == storyline:
            self.connections=prev_chap.connectins
            self.interactables=prev_chap.interactables
            self.knownledge=prev_chap.knownledge
            mapping={}

    def __setattr__(self, attr, ret):
        if issubclass(type(ret), interactable):
            ret.name=attr
        elif attr.startswith("__"):
            pass
        else:
            ret=interactable(ret)
            ret.name=attr
        return super(storyline, self).__setattr__(attr, ret)

    def register_interactables(self, interactables):
        for i in interactables:
            if i in self.interactables:
                raise ArgumentError("This interactable already exists!")
