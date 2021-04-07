import pytest
from model.individual import Individual as Ind

class TestSurvivalFeature(object):

	def test_individuals_have_survival_function(self):
		assert hasattr(Ind(), "survive"), "individuals cannot survive"
		assert callable(getattr(Ind(), "survive"))

	def test_individuals_can_die(self):
		self.ind = Ind()
		self.ind.survive()
		assert hasattr(self.ind, "alive")
		assert self.ind.alive is not None
		assert type(self.ind.alive) is bool