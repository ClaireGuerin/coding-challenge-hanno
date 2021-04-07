import pytest
from model.individual import Individual as Ind

class TestConsumptionFunction(object):

	def test_individuals_can_consume_resources(self):
		assert hasattr(Ind(), "consume"), "individual has no consumption method"
		assert callable(getattr(Ind(), "consume"))

	def test_individual_has_access_to_resources(self):
		try:
			Ind(res=10)
		except TypeError as e:
			assert False, "no resources available"


	def test_consumption_depends_on_resources_no_neighbours(self):
		assert False, "write this test"

	def test_consumption_depends_on_vigilance_no_neighbours(self):
		assert False, "write this test"

	def test_individual_knows_neighbours_consumption_level(self):
		assert False, "write this test"

	def test_consumption_depends_on_neighbours_vigilance(self):
		assert False, "write this test"