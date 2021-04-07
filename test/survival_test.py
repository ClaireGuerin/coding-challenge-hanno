import pytest
from model.individual import Individual as Ind

class TestSurvivalFeature(object):

	def test_individuals_have_survival_function(self):
		assert hasattr(Ind(), "survive"), "individuals cannot survive"
		assert callable(getattr(Ind(), "survive"))