import datetime

class Logger:
	def __init__(self):
		self._logs = []
		self._logs_max_size = 5
		self._last_log_added_time = datetime.datetime.now()
		self._log_duration = 0.5
	def print_all_logs(self):
		interval = datetime.datetime.now() - self._last_log_added_time
		if interval.total_seconds() > self._log_duration:
			self._logs = []
		# print empty lines
		for i in range(self._logs_max_size - len(self._logs)):
			print("")
		# print logs
		for log in self._logs:
			print(log)
	def add_log(self, log : str):
		self._last_log_added_time = datetime.datetime.now()
		self._logs.append(log)
