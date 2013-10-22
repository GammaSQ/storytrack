class Group_Base(object):
    pass

class Group(Group_Base):
    def __init__(self):
        self.events=set()
        self.members=set()
        self.hands=set()

    def handlers(self):
        ret= self.hands.copy()
        for mem in self.members:
            ret |= mem.handlers()
        return ret

    def reg_event(self, event):
        self.events.add(event)

    def drop_event(self, event):
        self.events.discard(event)

    def join(self, mem):
        self.members.add(mem)
    def leave(self, mem):
        self.members.remove(mem)