import pytest
from model.individual import Individual as Ind
from model.population import Population as Pop

class TestReproductionFunction(object):

	def test_individual_can_reproduce(self):
		assert hasattr(Ind(), "reproduce"), "ind cannot reproduce"

	def test_fertility_returns_positive_float(self):
		self.fakepop = Pop()
		self.fakepop.create(10)
		
		for ind in range(len(self.fakepop.individuals)):
			indiv = self.fakepop.individuals[ind]
			setattr(indiv, "storage", 1 + 9 * ind) 
			indiv.reproduce()
			assert type(indiv.fertility) is float
			assert indiv.fertility >= 0

	def test_reproduction_gives_offspring_number(self):
		self.indiv = Ind()
		
		self.indiv.reproduce()
		assert self.indiv.offspring != None, "No offspring number generated"
		assert type(self.indiv.offspring) is int, "Offspring number of wrong format: {0} instead of integer".format(type(self.indiv.offspring))
		assert self.indiv.offspring >= 0, "Offspring number cannot be negative"

	def test_reproduction_is_seed_dependent(self, pseudorandom):
		self.nIndividuals = 1000
		self.fakepop = Pop()
		self.fakepop.create(self.nIndividuals)

		offspring = []

		for ind in self.fakepop.individuals:
			setattr(ind, "fertility", 4)
			pseudorandom(0)
			ind.reproduce()
			offspring.append(ind.offspring)

		assert all([x == offspring[0] for x in offspring]), "number of offspring differs with same seed, {0}".format(set(offspring))

			
	def test_reproduction_follows_a_poisson_distribution(self, pseudorandom):
		#http://www2.stat-athens.aueb.gr/~exek/papers/Xekalaki-Statistician2000(355-382)ft.pdf
		pseudorandom(0)
		
		self.nIndividuals = 1000
		self.fakepop = Pop()
		self.fakepop.create(self.nIndividuals)
		self.explambda = 4
		
		offspringPerInd = []
		for ind in self.fakepop.individuals:
			setattr(ind, "fertility", self.explambda)
			ind.reproduce()
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
			expectedCount.append(self.nIndividuals * expProbability)
						
		chisq, pval = scistats.chisquare(observedCount, expectedCount)
		assert len(expectedCount) == len(observedCount), "len obs = {0}, len exp = {1}".format(len(observedCount), len(expectedCount))
		#assert sum(expectedCount) == sum(observedCount), "n obs = {0}, n exp = {1}".format(sum(observedCount), sum(expectedCount))
		assert pval > 0.05, "Test for goodness of fit failed: obs = {0}, exp = {1}".format(observedCount, expectedCount)	