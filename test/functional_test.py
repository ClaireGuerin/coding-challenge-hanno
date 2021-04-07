import pytest
import os
from model.population import Population as Pop

class TestSimpleRun(object):

	# The user gives a number of parameters necessary to run the simulation
	def test_there_is_a_parameter_file(self):
		self.filesListRoot = os.listdir(".")
		assert "parameters.txt" in self.filesListRoot, "parameter file missing in root"

	# A grid is created

	# The grid is a square of the size given in parameters

	# A population of prey individuals is created, of the size given in parameters

	# The user launches the simulation
	def test_simulation_can_be_launched(self):
		self.population = Pop()

		try:
		 	self.population.launch()
		except AttributeError as e:
			assert False, "population has no launching method"

	# The simulation runs for the number of generations given in paramaters. An output file is created with information on vigilance level in the population

	def test_simulation_runs_for_n_gen(self):
		self.population = Pop()
		self.population.launch()
		self.filesListRootOut = os.listdir(".")

		assert "vigilance_out.txt" in self.filesListRootOut, "no output file"

	# The output file contains exactly the number of lines that corresponds to the number of generations

	# A message is generated, informing the user that the simulation has successfully completed.
