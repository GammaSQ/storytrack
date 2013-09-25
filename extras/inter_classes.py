from storycheck.engine import interactible

class character (interactible):
	def talk_options(self, actor=None):
		return self.options.keys()

	def talk(self, target):

		target.talk_to(self, modifications)