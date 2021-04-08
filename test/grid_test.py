import pytest
from numpy import array

class TestGridObject(object):

	def test_grid_has_cell_resources_info(self):
		self.dimension = 10
		self.grid = Grid(dim=self.dimension)
		assert hasattr(self.grid, "resources")
		assert type(self.grid.resources) is list
		assert self.grid.resources.shape
