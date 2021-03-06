import pytest
from model.individual import Individual as Ind
from model.population import Population as Pop
from collections import Counter
import math as m
import scipy.stats as scistats

class TestReproductionFunction(object):

	def test_individual_can_reproduce(self):
		assert hasattr(Ind(m=3), "reproduce"), "ind cannot reproduce"

	def test_fertility_returns_positive_float(self):
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create()
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "storage", 1 + 9 * ind) 
			indiv.reproduce(fecundity=2)
			assert type(indiv.fertility) is float
			assert indiv.fertility >= 0

	def test_fertility_increases_with_storage(self):
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create()

		fertility = 0
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "storage", 1 + 9 * ind) 
			indiv.reproduce(fecundity=2)
			assert indiv.fertility > fertility
			fertility = indiv.fertility

	def test_reproduction_gives_offspring_number(self):
		self.indiv = Ind(m=3)
		
		self.indiv.reproduce(fecundity=2)
		assert self.indiv.offspring != None, "No offspring number generated"
		assert type(self.indiv.offspring) is int, "Offspring number of wrong format: {0} instead of integer".format(type(self.indiv.offspring))
		assert self.indiv.offspring >= 0, "Offspring number cannot be negative"

	def test_offspring_number_increases_with_fertility(self):
		self.indLowFertility = Ind(m=3)
		self.indHighFertility = Ind(m=3)

		self.indLowFertility.storage = 1
		self.indLowFertility.reproduce(fecundity=0.5)
		self.indHighFertility.storage = 10
		self.indHighFertility.reproduce(fecundity=2)

		assert self.indLowFertility.offspring < self.indHighFertility.offspring, "high fertility should lead to higher offspring number"

	def test_reproduction_is_seed_dependent(self, pseudorandom):
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.nIndiv = 1000
		self.fakepop.create()

		offspring = []

		for ind in self.fakepop.individuals:
			setattr(ind, "storage", 4)
			pseudorandom(0)
			ind.reproduce(fecundity=2)
			offspring.append(ind.offspring)

		assert all([x == offspring[0] for x in offspring]), "number of offspring differs with same seed, {0}".format(set(offspring))

			
	def test_reproduction_follows_a_poisson_distribution(self, pseudorandom):
		#http://www2.stat-athens.aueb.gr/~exek/papers/Xekalaki-Statistician2000(355-382)ft.pdf
		pseudorandom(0)
		
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.nIndiv = 1000
		self.fakepop.create()
		self.explambda = 8
		
		offspringPerInd = []
		for ind in self.fakepop.individuals:
			setattr(ind, "storage", 4)
			ind.reproduce(fecundity=2)
			offspringPerInd.append(ind.offspring)
		
		d = Counter(offspringPerInd)
		a, b = list(d.keys()), list(d.values())
		maxCount = max(a)
		observedCount = []
		expectedCount = []
		
		for k in range(maxCount):
			if k in a:
				observedCount.append(d[k])
			else:
				observedCount.append(0)
			
			expProbability = m.pow(m.e, (-self.explambda)) * (m.pow(self.explambda, k)) / m.factorial(k)
			expectedCount.append(self.fakepop.nIndiv * expProbability)
						
		chisq, pval = scistats.chisquare(observedCount, expectedCount)
		assert len(expectedCount) == len(observedCount), "len obs = {0}, len exp = {1}".format(len(observedCount), len(expectedCount))
		#assert sum(expectedCount) == sum(observedCount), "n obs = {0}, n exp = {1}".format(sum(observedCount), sum(expectedCount))
		assert pval > 0.05, "Test for goodness of fit failed: obs = {0}, exp = {1}".format(observedCount, expectedCount)	