import pytest
from model.population import Population as Pop
from model.individual import Individual as Ind
from model.grid import Grid
import numpy as np
import gc
import os

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

	def test_population_individuals_are_unlinked(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()

		assert len(set(self.pop.individuals)) == self.pop.nIndiv

	def test_population_has_life_cycle(self):
		assert hasattr(Pop(), "lifeCycle")
		assert callable(getattr(Pop(), "lifeCycle"))	

	# def test_share_calculated_and_assigned_to_grid(self):
	# 	assert False, "write this test"

	# def test_pool_is_wiped_out_at_beginning_of_cycle(self):
	# 	assert False, "write this test"

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
		self.pop.nIndiv = 1000
		self.pop.gridSize = 60
		self.pop.create()

		coord = []
		for ind in self.pop.individuals:
			coord.append(ind.coordinates)

		self.pop.explore()

		newCoord = []
		for ind in self.pop.individuals:
			newCoord.append(ind.coordinates)

		assert all([coord[x] == newCoord[x] for x in range(len(coord))]) == False

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
		coord = []

		for ind in self.pop.individuals:
			ind.alive = False
			coord.append(ind.coordinates)

		self.pop.explore()
		
		newCoord = []
		for ind in self.pop.individuals:
			newCoord.append(ind.coordinates)

		assert all([coord[x] == newCoord[x] for x in range(len(coord))])


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
		self.pop.grid.share = np.full([self.pop.gridSize, self.pop.gridSize], 0.8)

		for i in self.pop.individuals:
			i.vigilance = 0

		self.pop.gatherAndSurvive()

		for i in self.pop.individuals:
			assert i.storage > 0

	def test_only_live_individuals_gather_and_survive(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()
		self.pop.explore()

		for ind in self.pop.individuals:
			ind.alive = False

		self.pop.gatherAndSurvive()
		
		for ind in self.pop.individuals:
			assert ind.alive == False
			assert ind.storage == 0

	def test_population_has_a_routine(self):
		assert hasattr(Pop(), "routine")
		assert callable(getattr(Pop(), "routine"))

	def test_population_routine_changes_share_grid(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create()

		shareG = self.pop.grid.share

		self.pop.routine()

		compareGrids = self.pop.grid.share == shareG

		assert compareGrids.all() == False

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
		assert type(self.pop.nextGeneration) is list
		assert len(self.pop.nextGeneration) > 0

		for elem in self.pop.nextGeneration:
			assert type(elem) is int
			assert elem in range(10)

		gc.collect()

	def test_pool_is_a_mix_of_individuals(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.initRes = 10
		self.pop.create()
		self.pop.routine()

		for ind in self.pop.individuals:
			ind.alive = True

		self.pop.reproduce()
		assert len(set(self.pop.nextGeneration)) > 1, "ids missing in {0}".format(set(self.pop.nextGeneration))

		gc.collect()

	def test_only_live_individuals_reproduce(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.initRes = 10
		self.pop.create()
		self.pop.routine()

		for ind in self.pop.individuals:
			ind.alive = False
		self.pop.individuals[0].alive = True

		self.pop.reproduce()
		#assert len(set(self.pop.nextGeneration)) > 1, "ids missing in {0}".format(set(self.pop.nextGeneration))
		assert len(set(self.pop.nextGeneration)) == 1, "there should be only one id in {0}".format(set(self.pop.nextGeneration))
		assert self.pop.nextGeneration.count(0) == self.pop.nIndiv, "only ind #0 should reproduce, not {0}".format(set(self.pop.nextGeneration))

		gc.collect()

	def test_death_counter(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.predation = 1
		self.pop.create()

		for ind in self.pop.individuals:
			ind.vigilance = 0

		self.pop.routine()
		for ind in self.pop.individuals:
			assert ind.alive == False

		self.pop.reproduce()

		assert self.pop.deathCount == 10

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

	def test_update_returns_population_vigilance_info(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()
		self.pop.routine()
		self.pop.reproduce()
		self.pop.update()

		assert hasattr(self.pop, "vigilance")
		assert self.pop.vigilance is not None
		assert type(self.pop.vigilance) is float
		assert 0 <= self.pop.vigilance <= 1

	def test_population_vigilance_is_correct(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()
		self.pop.routine()
		self.pop.reproduce()
		self.pop.update()

		collectVigilances = []

		for ind in self.pop.individuals:
			collectVigilances.append(ind.vigilance)

		assert self.pop.vigilance == pytest.approx(np.mean(collectVigilances), 0.1)

	def test_lam_error_when_resources_too_big(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.initRes = 20000000000000000000
		self.pop.create()
		try:
			self.pop.lifeCycle()
		except ValueError as e:
			assert str(e) == 'lam value too large', "This program should fail at poisson random draw, not '{0}'".format(e)

	def test_resources_crash_when_too_large(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.initRes = 20
		self.pop.growth = 100
		self.pop.create()
		self.pop.lifeCycle()

		for cell in np.nditer(self.pop.grid.resources):
			assert cell <= self.pop.initRes, "resources too large, should have crashed"

	def test_population_keeps_track_of_ecological_time(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()

		assert hasattr(self.pop, "ecoTime"), "population must keep track of its ecological time!"

	def test_ecological_time_correctly_assessed(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()
		self.pop.lifeCycle()
		ngen = 5

		assert self.pop.ecoTime == self.pop.routineSteps, "one life cycle should be {0} units of ecological time, not {1}".format(self.pop.routineSteps, self.pop.ecoTime)

		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()
		for i in range(ngen):
			self.pop.lifeCycle()

		assert self.pop.ecoTime == self.pop.routineSteps * ngen, "{2} life cycles should be {0} units of ecological time, not {1}".format(self.pop.routineSteps * 10, self.pop.ecoTime, ngen)

	def test_population_keeps_track_of_resources_over_life_cycle(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()

		assert hasattr(self.pop, "ecologyShortHistory"), "population must keep track of its ecological history!"

	def test_resources_info_augmented_at_each_routine(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()
		for i in range(self.pop.routineSteps):
			self.pop.routine()

		assert self.pop.ecologyShortHistory.shape == ((self.pop.gridSize ** 2) * self.pop.routineSteps, 4)

	def test_population_keeps_track_of_exploration_over_life_cycle(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.create()

		assert hasattr(self.pop, "explorationShortHistory"), "population must keep track of its exploration history!"

	def test_exploration_info_augmented_at_each_routine(self):
		self.pop = Pop(par="test/test/parameters.txt")
		self.pop.predation = 0
		self.pop.create()
		for i in range(self.pop.routineSteps):
			self.pop.routine()

		assert self.pop.explorationShortHistory.shape == (self.pop.nIndiv * self.pop.routineSteps, 3)