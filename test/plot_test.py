import pytest
from model.population import Population as Pop
import matplotlib.pyplot as plt

class TestPlottingFunction(object):

	def test_population_has_plotting_option(self):
		self.pop = Pop("test/test/parameters.txt",dev='on')
		self.pop.create()
		self.pop.launch()

		assert plt.get_fignums()

# xdata = []
# ydata = []
# plt.show()
# axes = plt.gca()
# axes.set_xlim(0, self.nGen)
# axes.set_ylim(0, 1)
# line, = axes.plot(xdata, ydata, 'k-')
# xdata.append(gen)
# ydata.append(self.vigilance)
# line.set_xdata(xdata)
# line.set_ydata(ydata)
# plt.draw()
# plt.show()