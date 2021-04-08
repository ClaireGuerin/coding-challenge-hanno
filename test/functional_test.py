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

	# The simulation runs for the number of generations given in parameters. An output file is created with information on vigilance level in the population

	def test_simulation_runs_for_n_gen(self):
		self.population = Pop()
		self.population.launch()
		self.filesListRootOut = os.listdir(".")

		assert "vigilance_out.txt" in self.filesListRootOut, "no output file"
		os.remove('vigilance_out.txt')

	# The output file contains exactly the number of lines that corresponds to the number of generations

	def test_simulation_runs_for_exact_generations(self):
		self.population = Pop(par="test/test/parameters.txt")
		self.population.launch()

		with open("vigilance_out.txt", "r") as fOut:
			lineCount = len(fOut.readlines())

		assert lineCount == 10, "wrong number of lines from file reading"
		os.remove('vigilance_out.txt')

	# A message is generated, informing the user that the simulation has successfully completed.
