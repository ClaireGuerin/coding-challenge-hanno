import pytest
import numpy as np
from model.grid import Grid

class TestGridObject(object):

	def test_grid_knows_own_dimensions(self):
		self.grid = Grid(dim=4, init=2)
		assert self.grid.dimension == 4

	def test_grid_has_cell_resources_info(self):
		self.dimension = 10
		self.grid = Grid(dim=self.dimension, init=2)
		assert hasattr(self.grid, "resources")
		assert type(self.grid.resources) is np.ndarray
		assert self.grid.resources.shape == (self.dimension, self.dimension)

	def test_cell_resources_correct_format(self):
		self.grid = Grid(dim=10, init=2)
		assert self.grid.resources.dtype == np.float32

	def test_grid_has_cell_resource_sharing_info(self):
		self.dimension = 10
		self.grid = Grid(dim=self.dimension, init=2)
		assert hasattr(self.grid, "share")
		assert type(self.grid.share) is np.ndarray
		assert self.grid.share.shape == (self.dimension, self.dimension)

	def test_cell_resource_sharing_correct_format(self):
		self.grid = Grid(dim=10, init=2)
		assert self.grid.share.dtype == np.float32

	def test_resources_get_initialized(self):
		self.grid = Grid(dim=10, init=2)
		assert hasattr(self.grid, "initialResources")
		assert self.grid.initialResources is not None
		assert type(self.grid.initialResources) is int
		assert self.grid.initialResources > 0

	def test_resources_grid_gets_correct_initial_value(self):
		self.grid = Grid(dim=10, init=2)

		for cell in np.nditer(self.grid.resources):
			assert pytest.approx(cell) == 2

	def test_grid_grows_resources_back(self):
		assert False, "write this test"
