class Group_Base(object):
    pass

class Group(Group_Base):
    def __init__(self):
        events={}
        members={}

    def event(self, event):
        for member in members.vals():
            quer=member.handle(event):
            if quer and quer == 'catch':
                break
