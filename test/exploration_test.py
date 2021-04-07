import pytest
from model.individual import Individual as Ind

class TestExplorationFunction(object):

	def test_individual_can_explore_grid(self):
		assert hasattr(Ind(), "explore"), "ind cannot explore"
		assert callable(getattr(Ind(), "explore")), "explore not a method"

	def test_individuals_make_steps(self):
		self.ind = Ind()
		gridSide=6
		self.ind.placeOnGrid(m=gridSide)

		storeStepsH = [99]*10
		storeStepsV = [99]*10
		
		for i in range(10):
			before = self.ind.coordinates
			self.ind.explore(m=gridSide)
			after = self.ind.coordinates
			storeStepsH[i] = before[0] - after[0]
			storeStepsV[i] = before[1] - after[1]

		assert any([x!=0 for x in storeStepsH]), "individual does not change horizontal"
		assert any([x!=0 for x in storeStepsV]), "individual does not change vertical"

	def test_steps_are_between_minus_one_and_one(self):
		self.ind = Ind()
		gridSide = 6
		self.ind.placeOnGrid(m=gridSide)

		storeStepsH = []
		storeStepsV = []
		
		for i in range(10):
			before = self.ind.coordinates
			self.ind.explore(m=gridSide)
			after = self.ind.coordinates
			storeStepsH.append(before[0] - after[0])
			storeStepsV.append(before[1] - after[1])

		assert all([x in [-1,0,1] for x in storeStepsH]), "wrong horizontal step size in {0}".format(storeStepsH)
		assert all([x in [-1,0,1] for x in storeStepsV]), "wrong vertical step size"

	def test_steps_are_bounded(self):
		self.ind = Ind()
		gridSide = 6

		self.ind.coordinates = [1,1]

		storeCoordH = []
		storeCoordV = []
		
		for i in range(10):
			self.ind.explore(m=gridSide)
			storeCoordH.append(self.ind.coordinates[0])
			storeCoordV.append(self.ind.coordinates[1])

		assert all([1 <= x <= gridSide for x in storeCoordH]), "stepped out of grid: {0}".format(storeCoordH)
		assert all([1 <= x <= gridSide for x in storeCoordV]), "stepped out of grid: {0}".format(storeCoordV)

		# reset for upper boundary

		self.ind.coordinates = [gridSide,gridSide]

		storeCoordH = []
		storeCoordV = []
		
		for i in range(10):
			self.ind.explore(m=gridSide)
			storeCoordH.append(self.ind.coordinates[0])
			storeCoordV.append(self.ind.coordinates[1])

		assert all([1 <= x <= gridSide for x in storeCoordH]), "stepped out of grid: {0}".format(storeCoordH)
		assert all([1 <= x <= gridSide for x in storeCoordV]), "stepped out of grid: {0}".format(storeCoordV)