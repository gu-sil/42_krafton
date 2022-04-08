class Actor:
	def __init__(self):
		self._x = 0
		self._y = 0
		self._ch = ""

	def __init__(self, x : int, y : int):
		self._x = x
		self._y = y
		self._ch = ""

	def __init__(self, x : int, y : int, ch : str):
		self._x = x
		self._y = y
		self._ch = ch

	def start(self):
		pass

	def update(self):
		pass

	def render(self):
		pass

