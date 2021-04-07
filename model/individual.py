import random
import numpy.random as rd
from operator import add

class Individual(object):

	def __init__(self):
		self.vigilance = float(0.5)
		self.coordinates = [-1,-1]
		self.mutant = None

	def placeOnGrid(self, m):
		self.coordinates = [random.randint(1, m), random.randint(1, m)]

	def mutate(self, mutRate, mutStep, bounded=True):
		self.mutant = bool(rd.binomial(1, mutRate))
		self.deviate(mutStep)
		self.applyMutation(self.mutationDeviation, bounded)

	def deviate(self, mutStep):
		if self.mutant:
			dev = rd.normal(0, mutStep)
		else:
			dev = 0.0
		self.mutationDeviation = dev

	def applyMutation(self, dev, bound):
		unboundedphen = self.vigilance + dev
		if bound == False:
			setattr(self, "vigilance", unboundedphen)
		else:
			boundedphen = min(max(unboundedphen,0.0),1.0)
			setattr(self, "vigilance", boundedphen)

	def explore(self, m):
		steps = [random.randint(-1, 1), random.randint(-1, 1)]
		self.coordinates = list(map(add, self.coordinates, steps))