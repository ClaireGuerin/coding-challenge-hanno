import pytest
from model.individual import Individual as Ind

class TestConsumptionFunction(object):

	def test_individuals_can_gather_resources(self):
		assert hasattr(Ind(), "gather"), "individual has no consumption method"
		assert callable(getattr(Ind(), "gather"))

	def test_individual_has_access_to_storage(self):
		assert hasattr(Ind(), "storage"), "individual cannot store resources"
		self.ind = Ind()
		assert self.ind.storage == 0, "individual initial resource storage should be empty"

	def test_gathering_depends_on_resources_no_neighbours(self):
		self.ind = Ind()
		self.ind.gather(resources = 5, share = 1-self.ind.vigilance, efficiency = 0.9)
		firstGathering = self.ind.storage
		self.ind.gather(resources = 10, share = 1-self.ind.vigilance, efficiency = 0.9)

		assert self.ind.storage > firstGathering
		assert (self.ind.storage - firstGathering) > firstGathering

	def test_gathering_depends_on_vigilance_no_neighbours(self):
		self.ind = Ind()
		assert self.ind.storage == 0
		self.ind.vigilance = 0.1
		self.ind.gather(resources = 6, share = 1-self.ind.vigilance, efficiency = 0.9)
		firstGathering = self.ind.storage
		expect = (1-0.1)*0.9*6
		assert firstGathering == expect, "gathered {0} instead of {1}".format(firstGathering, expect)
		self.ind.vigilance = 0.8
		self.ind.gather(resources = 6, share = 1-self.ind.vigilance, efficiency = 0.9)

		assert self.ind.storage > firstGathering
		assert (self.ind.storage - firstGathering) < firstGathering

	def test_gathering_depends_on_neighbours_vigilance(self):
		self.ind = Ind()
		self.ind.gather(resources = 6, share = (1-self.ind.vigilance+0.9)/2, efficiency = 0.9)
		firstGathering = self.ind.storage
		self.ind.gather(resources = 6, share = (1-self.ind.vigilance+0.7*2)/3, efficiency = 0.9)

		assert self.ind.storage > firstGathering
		assert (self.ind.storage - firstGathering) < firstGathering