# -*- coding: utf-8 -*-
"""Individual Prey

Stores and updates individual information and status such as coordinates or vigilance level.
Methods ar eindividual actions, such as explore, survive, gather, reproduce.
"""

import random
import numpy.random as rd
from operator import add

class Individual(object):

	def __init__(self, m, v=0.5):
		"""Initialize individual basic attributes

		Coordinates are randomly assigned based on the grid size (m*m)
		"""
		self.m = m
		self.vigilance = float(v)
		self.coordinates = [random.randint(0, self.m-1), random.randint(1, self.m-1)]
		self.mutant = None
		self.storage = 0
		self.alive = True

	def mutate(self, mutRate, mutStep, bounded=True):
		""" Mutate vigilance level
		Return nothing
		Update self.mutant and self.vigilance values
		"""
		self.mutant = bool(rd.binomial(1, mutRate))
		self.deviate(mutStep)
		self.applyMutation(self.mutationDeviation, bounded)

	def deviate(self, mutStep):
		""" Deviation from phenotype
		Return nothing
		Create self.mutationDeviation value.
		"""
		if self.mutant:
			dev = rd.normal(0, mutStep)
		else:
			dev = 0.0
		self.mutationDeviation = dev

	def applyMutation(self, dev, bound):
		""" Change phenotype value and apply boundaries if necessary.
		Return nothing
		Update self.vigilance value
		"""
		unboundedphen = self.vigilance + dev
		if bound == False:
			setattr(self, "vigilance", unboundedphen)
		else:
			boundedphen = min(max(unboundedphen,0.0),1.0)
			setattr(self, "vigilance", boundedphen)

	def explore(self):
		""" Move individual on the grid
		Return nothing
		Update self.coordinates values
		Current position can be changed by -1, 0 or 0 on both axes.
		If change is 0 on both x and y axis, the individual stays where they are.
		"""
		steps = [random.randint(-1, 1), random.randint(-1, 1)]
		unboundedCoordinates = list(map(add, self.coordinates, steps))
		tmpcoord = list(map(lambda x: min(max(x,0), self.m-1), unboundedCoordinates))
		setattr(self, "coordinates", tmpcoord)

	def survive(self, p):
		""" Does the individual survive or not?
		Return nothing
		Update self.alive value. If True, the individual is alive, if False, the individual is dead.
		Survival depends on vigilance and basal predation risk, i.e. the probability to get eaten in absence of vigilance.
		"""
		predationRisk = p * (1 - self.vigilance) # 0 <= p <= 1 is the basal predation risk 
		self.alive = bool(rd.binomial(1, 1-predationRisk))

	def gather(self, resources, share, efficiency):
		""" Gather and store resources
		Return nothing
		Update self.storage value.
		Add gathered resources to existing storage.
		"""
		self.storage += efficiency * resources * share # share = SUM(1-v_i)/(gamma*n), gamma = competition parameter

	def reproduce(self, fecundity):
		""" Reproduce
		Return nothing
		Create self.fertility and self.offspring values.
		Calculate fertility based on amount of resources stored in self.storage.
		Draw offspring number from Poisson distribution with lambda = mean = variance = fertility.
		"""
		residualFecundity = 0.0001
		self.fertility = float(residualFecundity + fecundity * self.storage)
		self.offspring = rd.poisson(max(0,self.fertility))