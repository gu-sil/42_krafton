import actor

class MainCharacter(actor.Actor):
	def __init__(self, x : int, y : int, ch : str):
		super().__init__(x, y, ch)

	def start(self):
		super().start()

	def update(self):
		super().update()

	def render(self):
		super().render()
