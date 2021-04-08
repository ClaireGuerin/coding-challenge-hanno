import random
import numpy.random as rd
from operator import add

class Individual(object):

	def __init__(self,m):
		self.m = m
		self.vigilance = float(0.5)
		self.coordinates = [random.randint(0, self.m-1), random.randint(1, self.m-1)]
		self.mutant = None
		self.storage = 0

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

	def explore(self):
		steps = [random.randint(-1, 1), random.randint(-1, 1)]
		unboundedCoordinates = list(map(add, self.coordinates, steps))
		tmpcoord = list(map(lambda x: min(max(x,0), self.m-1), unboundedCoordinates))
		setattr(self, "coordinates", tmpcoord)

	def survive(self, p):
		# p is the basal predation risk, i.e. the probability to get eaten in absence of vigilance
		# 0 <= p <= 1
		predationRisk = p * (1 - self.vigilance)
		self.alive = bool(rd.binomial(1, 1-predationRisk))

	def gather(self, resources, share, efficiency):
		# share = SUM(1-v_i)/(gamma*n)
		# where gamma is the competition parameter
		self.storage += efficiency * resources * share

	def reproduce(self, fecundity):
		residualFecundity = 0.0001
		self.fertility = float(residualFecundity + fecundity * self.storage)
		self.offspring = rd.poisson(max(0,self.fertility))