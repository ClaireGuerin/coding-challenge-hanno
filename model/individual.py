import random

class Individual(object):

	def __init__(self):
		self.vigilance = float(0.5)
		self.coordinates = [-1,-1]

	def placeOnGrid(self, m):
		self.coordinates = [random.randint(1, m), random.randint(1, m)]