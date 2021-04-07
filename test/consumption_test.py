import pytest
from model.individual import Individual as Ind

class TestConsumptionFunction(object):

	def test_individuals_can_consume_resources(self):
		assert hasattr(Ind(), "consume"), "individual has no consumption method"
		assert callable(getattr(Ind(), "consume"))

	def test_individual_has_access_to_resources_and_storage(self):
		assert hasattr(Ind(), "resources"), "individual has no access to resources"
		assert hasattr(Ind(), "storage"), "individual cannot store resources"
		self.ind = Ind()
		assert self.ind.storage == 0, "individual initial resource storage should be empty"

	def test_consumption_depends_on_resources_no_neighbours(self):
		assert False, "write this test"

	def test_consumption_depends_on_vigilance_no_neighbours(self):
		assert False, "write this test"

	def test_individual_knows_neighbours_consumption_level(self):
		assert hasattr(Ind(), "competition"), "individual should be subject to competition"

	def test_consumption_depends_on_neighbours_vigilance(self):
		assert False, "write this test"

	def test_resources_return_to_none_after_consumption(self):
		assert False, "write this test"