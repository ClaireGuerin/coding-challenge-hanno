import pytest
from model.population import Population as Pop
import random as rd
import numpy.random as np
import os

@pytest.fixture
def pseudorandom():
	def _foo(n):
		rd.seed(n)
		np.seed(n)

	return _foo

@pytest.fixture
def clearOutputFiles():
	def _foo(vis=False):
		os.remove("output/vigilance_out.txt")
		os.remove("output/resources_out.txt")
		os.remove("output/exploration_out.txt")
		if vis:
			os.remove("output/vigilance_out.gif")
			os.remove("output/grid_out.gif")
			
	return _foo