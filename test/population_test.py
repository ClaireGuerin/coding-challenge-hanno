from model.population import Population as Pop
from model.individual import Individual as Ind
from model.grid import Grid
import numpy as np
import gc

class TestPopulationObject(object):

	def test_population_has_individual_instances(self):
		self.pop = Pop("test/test/parameters.txt")

		assert hasattr(self.pop, "create"), "cannot create pop"
		self.pop.create(2)
		assert hasattr(self.pop, "individuals"), "no indivs in this pop"

	def test_population_has_correct_density(self):
		self.pop = Pop("test/test/parameters.txt")

		d1 = 2
		self.pop.create(d1)

		assert type(self.pop.individuals) is list
		assert len(self.pop.individuals) == d1
		for i in self.pop.individuals:
			assert type(i) is Ind

		d2 = 10
		self.pop.create(d2)

		assert type(self.pop.individuals) is list
		assert len(self.pop.individuals) == d2
		for i in self.pop.individuals:
			assert type(i) is Ind

	def test_population_has_life_cycle(self):
		assert hasattr(Pop(), "lifeCycle")
		assert callable(getattr(Pop(), "lifeCycle"))	

	# def test_share_calculated_and_assigned_to_grid(self):
	# 	assert False, "write this test"

	# def test_pool_is_wiped_out_at_beginning_of_cycle(self):
	# 	assert False, "write this test"

	def test_life_cycle_returns_output_info(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create(n=10)
		self.pop.lifeCycle()

		assert hasattr(self.pop, "vigilance")
		assert self.pop.vigilance is not None
		assert type(self.pop.vigilance) is float
		assert 0 <= self.pop.vigilance <= 1

	def test_population_creates_grid(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create(n=20)

		assert hasattr(self.pop, "grid")
		assert type(self.pop.grid) is Grid
		assert self.pop.grid.resources.shape == (self.pop.gridSize, self.pop.gridSize)

	def test_population_explores_grid(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()

		assert hasattr(self.pop, "explore")

	def test_population_exploration_leads_to_change_in_coord(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create(n=10)

		coordH = []
		coordV = []

		for ind in self.pop.individuals:
			coordH.append(ind.coordinates[0])
			coordV.append(ind.coordinates[1])

		self.pop.explore()

		coordH2 = []
		coordV2 = []

		for ind in self.pop.individuals:
			coordH2.append(ind.coordinates[0])
			coordV2.append(ind.coordinates[1])

		assert any([x != y for x in coordH for y in coordH2])
		assert any([x != y for x in coordV for y in coordV2])

	def test_population_exploration_gives_share_info(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()
		self.pop.explore()
		m = self.pop.gridSize

		assert hasattr(self.pop, "ncell")
		assert type(self.pop.ncell) is np.ndarray
		assert self.pop.ncell.shape == (m,m)
		assert hasattr(self.pop, "vcell")
		assert type(self.pop.vcell) is np.ndarray
		assert self.pop.vcell.shape == (m,m)

	def test_only_live_individuals_explore(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()
		coordH = []
		coordV = []

		for ind in self.pop.individuals:
			ind.vigilance = 0
			coordH.append(ind.coordinates[0])
			coordV.append(ind.coordinates[1])


		self.pop.explore()
		
		coordH2= []
		coordV2 = []
		for ind in self.pop.individuals:
			coordH2.append(ind.coordinates[0])
			coordV2.append(ind.coordinates[1])

		assert all([x == y for x in coordH for y in coordH2])
		assert all([x == y for x in coordV for y in coordV2])


	def test_population_can_gather_vs_survive(self):
		assert hasattr(Pop(), "gatherAndSurvive")
		assert callable(getattr(Pop(), "gatherAndSurvive"))

		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()
		try:
			self.pop.gatherAndSurvive()
		except ValueError as e:
			assert False, "missing info: {0}".format(e)

	def test_gathering_gives_individuals_storage(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()

		for i in self.pop.individuals:
			i.vigilance = 0

		self.pop.gatherAndSurvive()

		for i in self.pop.individuals:
			assert i.storage > 0

	def test_population_has_a_routine(self):
		assert hasattr(Pop(), "routine")
		assert callable(getattr(Pop(), "routine"))

	def test_population_routine_changes_share_grid(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()

		shareG = self.pop.grid.share

		self.pop.routine()

		compareGrids = self.pop.grid.share != shareG

		assert compareGrids.all()

	def test_population_routine_changes_resources_grid(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()

		resG = self.pop.grid.resources

		self.pop.routine()

		compareGrids = self.pop.grid.resources != resG

		assert compareGrids.all()

	def test_reproduction_at_population_level(self):
		assert hasattr(Pop(), "reproduce")
		assert callable(getattr(Pop(), "reproduce"))

		gc.collect()

	def test_reproduction_creates_pool(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()
		self.pop.routine()
		self.pop.reproduce()

		assert hasattr(self.pop, "nextGeneration"), "population pool does not exist"
		assert type(self.pop.pool) is list
		assert len(self.pop.pool) > 0

		for elem in self.pop.pool:
			assert type(elem) is int
			assert elem in range(10)

		gc.collect()

	# def test_pool_is_offspring_per_individual(self):
	# 	self.pop = Pop(par="test/test/parameters.txt")
	# 	self.pop.create()
	# 	self.pop.routine()
	# 	self.pop.reproduce()

	# 	count = []

	# 	for ind in range(self.pop.nIndiv):
	# 		indiv = self.pop.individuals[ind]
	# 		count.append(indiv.offspring)

	# 	for ind in range(self.pop.nIndiv):
	# 		indiv = self.pop.individuals[ind]
	# 		assert indiv.offspring == self.pop.pool.count(ind), "wrong offspring number for individual {1} in {0}. Counts: {2}".format(self.pop.pool, ind, count)

	def test_population_gets_updated_at_new_gen(self):
		assert hasattr(Pop(), "update")
		assert callable(getattr(Pop(), "update"))

	def test_update_replaces_old_gen_with_new_gen(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()
		self.pop.routine()
		self.pop.reproduce()
		oldgen = self.pop.individuals
		self.pop.update()

		assert len(self.pop.individuals) == self.pop.nIndiv
		assert self.pop.individuals != oldgen


