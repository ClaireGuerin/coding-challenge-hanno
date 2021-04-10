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

		assert hasattr(self.population, "launch"), "population has no launching method"
		assert callable(getattr(self.population, "launch"))
	# The simulation runs for the number of generations given in parameters. An output file is created with information on vigilance level in the population

	def test_simulation_returns_proper_output(self):
		self.population = Pop(par="test/test/parameters.txt")
		self.population.create()
		self.population.launch()
		self.filesListRootOut = os.listdir(".")

		assert "vigilance_out.txt" in self.filesListRootOut, "no vigilance output file"
		assert "resources_out.txt" in self.filesListRootOut, "no resources output file"
		assert "exploration_out.txt" in self.filesListRootOut, "no exploration output file"
		os.remove('vigilance_out.txt')
		os.remove('resources_out.txt')
		os.remove('exploration_out.txt')

	# The vigilance output file contains exactly the number of lines that corresponds to the number of generations

	def test_simulation_runs_for_exact_generations(self):
		self.population = Pop(par="test/test/parameters.txt")
		self.predation = 0
		self.population.create()
		self.population.launch()

		assert self.population.deathCount != self.population.nIndiv
		for ind in self.population.individuals:
			assert ind.alive

		with open("vigilance_out.txt", "r") as fOut:
			lineCount = len(fOut.readlines())

		assert lineCount == 10, "wrong number of lines from file reading"
		os.remove('vigilance_out.txt')

	# The resources output file contains exactly the number of lines that corresponds to the number of combinations of total routine time steps * grid * grid

	# A message is generated, informing the user that the simulation has successfully completed.
