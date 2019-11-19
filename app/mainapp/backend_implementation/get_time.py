from datetime import datetime

class GetTime():
	def __init__(self):
		self.application_start_time = self.get_current_time()

	@staticmethod
	def get_current_time():
		return datetime.now().strftime("%Y-%m-%d %H:%M:%S")