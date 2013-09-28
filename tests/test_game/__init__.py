class whitch (interactible):
    no_action += ['say', 'scream']
    def react_to_offer(self, actor, offer):
        if offer.value > 2:
            ret = menue()############
            self.say("Yes yes, good choice!")
            return ret
        else:
            self.screem("get away! that is worthless!")

    #@no_action
    def say(self, msg):
        print msg

    #@no_action
    def screem(self, msg):
        print msg.upper()