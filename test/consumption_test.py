import pytest
from model.individual import Individual as Ind

class TestConsumptionFunction(object):

	def test_individuals_can_consume_resources(self):
		assert hasattr(Ind(), "consume"), "individual has no consumption method"
		assert callable(getattr(Ind(), "consume"))