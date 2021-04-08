import pytest
from model.individual import Individual as Ind
import scipy.stats as scistats
import random

class TestSurvivalFeature(object):

	def test_individuals_have_survival_function(self):
		assert hasattr(Ind(m=3), "survive"), "individuals cannot survive"
		assert callable(getattr(Ind(m=3), "survive"))

	def test_individuals_can_die(self):
		self.ind = Ind(m=3)
		self.ind.survive(p=0.5)
		assert hasattr(self.ind, "alive")
		assert self.ind.alive is not None
		assert type(self.ind.alive) is bool

	def test_death_depends_on_predation_risk(self):
		self.ind = Ind(m=3)
		self.ind.vigilance = 0
		self.ind.survive(p=0)
		assert self.ind.alive == True

		self.ind.survive(p=1)
		assert self.ind.alive == False

	def test_death_depends_on_vigilance(self):
		self.ind = Ind(m=3)
		self.ind.vigilance = 0
		self.ind.survive(p=1)
		assert self.ind.alive == False

		self.ind.vigilance = 1
		self.ind.survive(p=1)
		assert self.ind.alive == True

	def test_average_survival_for_intermediate_vigilance(self):
		self.ind = Ind(m=3)
		self.ind.vigilance = random.random()
		
		deathCount = 0
		sampleSize = 1000

		for i in range(sampleSize):
			self.ind.survive(p=1)
			if not self.ind.alive:
				deathCount += 1

		stat1, pval1 = scistats.ttest_1samp([1] * deathCount + [0] * (sampleSize - deathCount), 1 - self.ind.vigilance)
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(deathCount/sampleSize, 1 - self.ind.vigilance)
		self.test = scistats.binom_test(deathCount, sampleSize, 1 - self.ind.vigilance, alternative = "two-sided")
		assert self.test > 0.05, "Success rate = {0} when predation rate = {1}".format(self.mutantCount/self.nIndividuals, 1 - self.ind.vigilance)