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