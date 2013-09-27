from storycheck.engine.interactables import interactible

class storyline(object):
    #self.map=[]
    def __init__(self, prev_chap=None):
        if prev_chap and type(prev_chap) == storyline:
            self.connections=prev_chap.connectins
            self.interactibles=prev_chap.interactibles
            self.knownledge=prev_chap.knownledge

    def __setattr__(self, attr, ret):
        if issubclass(type(ret), interactible):
            ret.name=attr
        elif attr.startswith("__"):
            pass
        else:
            ret=interactible(ret)
            ret.name=attr
        return super(storyline, self).__setattr__(attr, ret)

    def register_interactibles(self, interactibles):
        for i in interactibles:
            if i in self.interactibles:
                raise ArgumentError("This interactible already exists!")