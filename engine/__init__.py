class storyline:
	#self.map=[]
	def __init__(self, prev_chap=None):
		if prev_chap and type(prev_chap) == storyline:
			self.connections=prev_chap.connectins
			self.interactibles=prev_chap.interactibles
			self.knownledge=prev_chap.knownledge

	def register_interactibles(self, interactibles):
		for i in interactibles:
			if i in self.interactibles:
				raise ArgumentError("This interactible already exists!")