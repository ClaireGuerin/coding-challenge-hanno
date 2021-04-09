import pytest
from model.population import Population as Pop

class TestPlottingFunction(object):

	def test_population_has_plotting_option(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()
		try:
			self.pop.launch(dev='on')
		except TypeError as e:
			assert False, "allow for 'on' device to show plots"