import pytest
from model.population import Population as Pop
import os

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