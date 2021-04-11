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

	def test_simulation_returns_proper_output(self, clearOutputFiles):
		self.population = Pop(par="test/test/parameters.txt")
		self.population.create()
		self.population.launch()
		self.filesListRootOut = os.listdir("./output")

		assert "vigilance_out.txt" in self.filesListRootOut, "no vigilance output file"
		assert "resources_out.txt" in self.filesListRootOut, "no resources output file"
		assert "exploration_out.txt" in self.filesListRootOut, "no exploration output file"
		clearOutputFiles()

	# The vigilance output file contains exactly the number of lines that corresponds to the number of generations

	def test_simulation_runs_for_exact_generations(self, clearOutputFiles):
		self.population = Pop(par="test/test/parameters.txt")
		self.predation = 0
		self.population.create()
		self.population.launch()

		assert self.population.deathCount != self.population.nIndiv
		for ind in self.population.individuals:
			assert ind.alive

		with open("output/vigilance_out.txt", "r") as fOut:
			lineCount = len(fOut.readlines())

		assert lineCount == 10, "wrong number of lines from file reading"
		clearOutputFiles()

	# However, all individuals in the simulation die, leading to population extinction. The simulation stops and the output files are shorter.

	def test_simulation_stops_when_all_indivs_are_dead(self, clearOutputFiles):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.nGen = 5
		self.pop.predation = 1
		self.pop.create()

		for ind in self.pop.individuals:
			ind.vigilance = 0

		self.pop.launch()
		
		#assert self.pop.deathCount == self.pop.nIndiv, "there are {0} unexpected survivors".format(self.pop.nIndiv - self.pop.deathCount)
		with open("output/vigilance_out.txt", "r") as fOut:
			lineCount = len(fOut.readlines())
		assert lineCount == 1
		clearOutputFiles()


	# The resources output file contains exactly the number of lines that corresponds to the number of combinations of total routine time steps * grid * grid * number of generations

	def test_resources_output_right_length(self, clearOutputFiles):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.nGen = 5
		self.pop.predation = 0
		self.pop.create()
		self.pop.launch()
		
		with open("output/resources_out.txt", "r") as fOut:
			lineCount = len(fOut.readlines())
		assert lineCount == self.pop.nGen * self.pop.routineSteps * self.pop.gridSize * self.pop.gridSize
		clearOutputFiles()

	# When no individual dies, the the exploration output file contains exactly the number of lines that corresponds to the number of combinations of total routine time steps * number of individuals * number of generations

	def test_exploration_output_right_length(self, clearOutputFiles):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.nGen = 5
		self.pop.predation = 0
		self.pop.create()
		self.pop.launch()
		
		with open("output/exploration_out.txt", "r") as fOut:
			lineCount = len(fOut.readlines())
		assert lineCount == self.pop.nGen * self.pop.routineSteps * self.pop.nIndiv
		clearOutputFiles()

	# The user gets tired of tinkering with the code, and so uses run.py from command line to launch her simulation.

	def test_simulation_can_be_launched_from_command_line(self, clearOutputFiles):
		os.system("python run.py off")

		self.filesListRootOut = os.listdir("./output")

		assert "vigilance_out.txt" in self.filesListRootOut, "no vigilance output file"
		assert "resources_out.txt" in self.filesListRootOut, "no resources output file"
		assert "exploration_out.txt" in self.filesListRootOut, "no exploration output file"
		assert "grid_out.gif" not in self.filesListRootOut, "there should not be graphical output"
		assert "vigilance_out.gif" not in self.filesListRootOut, "there should not be graphical output"

		clearOutputFiles()

	@pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", 
reason="This test involves other languages that cannot be installed on Travis at the same time as Python")
	def test_command_line_takes_on_argument(self, clearOutputFiles):
		os.system("python run.py on")

		self.filesListRootOut = os.listdir("./output")

		assert "vigilance_out.txt" in self.filesListRootOut, "no vigilance output file"
		assert "resources_out.txt" in self.filesListRootOut, "no resources output file"
		assert "exploration_out.txt" in self.filesListRootOut, "no exploration output file"
		assert "grid_out.gif" in self.filesListRootOut, "there should be graphical output"
		assert "vigilance_out.gif" in self.filesListRootOut, "there should be graphical output"

		clearOutputFiles(vis=True)

	def test_when_no_argument_run_no_visual_with_message(self, clearOutputFiles):
		os.system("python run.py")

		self.filesListRootOut = os.listdir("./output")

		assert "vigilance_out.txt" in self.filesListRootOut, "no vigilance output file"
		assert "resources_out.txt" in self.filesListRootOut, "no resources output file"
		assert "exploration_out.txt" in self.filesListRootOut, "no exploration output file"
		assert "grid_out.gif" not in self.filesListRootOut, "there should be graphical output"
		assert "vigilance_out.gif" not in self.filesListRootOut, "there should be graphical output"

		clearOutputFiles()

	# A message is generated, informing the user that the simulation has successfully completed.
