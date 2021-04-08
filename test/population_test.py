from model.population import Population as Pop
from model.individual import Individual as Ind

class TestPopulationObject(object):

	def test_population_has_individual_instances(self):
		self.pop = Pop()

		assert hasattr(self.pop, "create"), "cannot create pop"
		self.pop.create(2)
		assert hasattr(self.pop, "individuals"), "no indivs in this pop"

	def test_population_has_correct_density(self):
		self.pop = Pop()

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

	def test_life_cycle_returns_offspring_pool(self):
		self.pop = Pop()
		self.pop.create(n=10)
		self.pop.lifeCycle()

		assert hasattr(self.pop, "pool"), "population pool does not exist"
		assert type(self.pop.pool) is list

		for elem in self.pop.pool:
			assert type(elem) is int
			assert elem in range(10)

	def test_pool_corresponds_to_number_of_offspring_per_individual(self):
		assert False, "write this test"

	def test_pool_is_wiped_out_at_beginning_of_cycle(self):
		assert False, "write this test"

	def test_life_cycle_returns_output_info(self):
		assert False, "write this test"