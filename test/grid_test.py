import pytest
import numpy as np
from model.grid import Grid

class TestGridObject(object):

	def test_grid_has_cell_resources_info(self):
		self.dimension = 10
		self.grid = Grid(dim=self.dimension)
		assert hasattr(self.grid, "resources")
		assert type(self.grid.resources) is np.ndarray
		assert self.grid.resources.shape == (self.dimension, self.dimension)

	def test_cell_resources_correct_format(self):
		self.grid = Grid(dim=10)
		assert self.grid.resources.dtype == np.float32

	def test_grid_has_cell_resource_sharing_info(self):
		self.dimension = 10
		self.grid = Grid(dim=self.dimension)
		assert hasattr(self.grid, "share")
		assert type(self.grid.share) is np.ndarray
		assert self.grid.share.shape == (self.dimension, self.dimension)

	def test_cell_resource_sharing_correct_format(self):
		self.grid = Grid(dim=10)
		assert self.grid.share.dtype == np.float32

