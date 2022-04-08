class Logger:
	def __init__(self):
		self._logs = []
	def print_all_logs(self):
		for log in self._logs:
			print(log)
	def add_log(self, log : str):
		self._logs.append(log)
	def clean_log(self):
		self._logs = []
