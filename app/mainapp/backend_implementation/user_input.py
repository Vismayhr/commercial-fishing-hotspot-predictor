import logging

class UserInput():
	def __init__(self, day, hour, dataset):
		self.day = day
		self.hour = hour
		self.dataset = dataset
		self.timestamp = self.generate_timestamp(day, hour)

	def generate_timestamp(self, day, hour):
		return str(day) + "-" + str(hour)
