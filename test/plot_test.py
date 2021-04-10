import pytest
from model.population import Population as Pop
import os

@pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", 
reason="These tests involve other languages that cannot be installed on Travis at the same time as Python")

class TestPlottingFunction(object):

	def test_population_has_plotting_option(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()
		try:
			self.pop.launch(dev='on')
		except TypeError as e:
			assert False, "allow for 'on' device to show plots"
		os.remove("vigilance_out.txt")
		os.remove("vigilance_out.gif")

	def test_gif_is_created_only_when_dev_on(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()
		self.pop.launch(dev='on')

		self.filesListRootOut = os.listdir(".")
		assert "vigilance_out.gif" in self.filesListRootOut, "no output gif created"
		os.remove("vigilance_out.txt")
		os.remove("vigilance_out.gif")

		self.pop.launch()
		self.filesListRootOut = os.listdir(".")
		assert "vigilance_out.gif" not in self.filesListRootOut, "should not have created output gif!"
		os.remove("vigilance_out.txt")

	def test_grid_gif_is_created(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()
		self.pop.launch(dev='on')

		self.filesListRootOut = os.listdir(".")
		assert "grid_out.gif" in self.filesListRootOut, "no output grid gif created"
		os.remove("vigilance_out.txt")
		os.remove("vigilance_out.gif")