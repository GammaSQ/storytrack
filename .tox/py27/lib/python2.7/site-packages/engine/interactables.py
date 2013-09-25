class interactible:
	def __init__(self, name, actions={}, reactions={}, posessions={}):
		self.name=name
		self.posessions=posessions
		self.actions=actions
		self.reactions=reactions

	def register_action(self, action={}):
		for key in action.keys():
			if key in self.action:
				raise KeyError("Action %s does already exist!"%key)
		self.actions += action

	def replace_action(self, action, replacement):
		self.actions[action]=replacement

	def register_reaction(self, reaction={}):
		for key in reaction.keys():
			if key in self.reaction:
				raise KeyError("Reaction %s does already exist!"%key)
		self.action += reaction

	def replace_action(self, reaction, replacement):
		self.reactions[reaction]=replacement

	def act_on(self, action, **kwargs):
		# Call the saved callback:
		act = self.actions[action](**kwargs)
		# If we want to act on a specific target (e.g. OPEN the TREASSURE),
		# it's reaction will be called. target has to be interactible.
		if target in kwargs:
			try:
				kwargs[target].react_to(action, self, act)
			except AttributeError:
				pass
		return act

	def react_to(self, action, actor, act=None):
		reaction, ret = self.reactions[action](actor, act)
		if reaction in self.action:
			# If the action needs a target, ret has to have a "target" key!
			# WARNING!!! DANGER OF ENTERNAL LOOP!
			self.act_on(action, **ret)
		return ret