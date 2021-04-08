import pytest
from model.individual import Individual as Ind
from model.population import Population as Pop
import scipy.stats as scistats
from operator import add
from statistics import mean
import gc

class TestMutationFunction(object):
			
	def test_mutation_function_takes_and_returns_phenotype(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create(n=1)
		self.indiv = self.pop.individuals[0]
		
		self.indiv.mutate(mutRate=0.5, mutStep=0.5)
		x = self.indiv.vigilance
		assert type(x) is float, "Phenotypic values ({0}) must be of type float, and not {1}".format(x, type(x))
		assert 0 <= x <= 1, "Phenotypic values must be in range [0,1]"
			
		gc.collect()
			
	def test_mutants_are_defined(self):
		self.pop = Pop("test/test/parameters.txt")
		self.pop.create(n=1)
		self.indiv = self.pop.individuals[0]
		
		self.indiv.mutate(mutRate=0.5, mutStep=0.5)
		assert hasattr(self.indiv, "mutant"), "We don't know if our individual is a mutant because it doesn't have this attribute"
		assert type(self.indiv.mutant) is bool
		
		gc.collect()

	def test_mutants_depend_on_seed(self, pseudorandom):
		self.nIndividuals = 1000
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create(n=self.nIndividuals)

		mutants = []

		for ind in self.fakepop.individuals:
			pseudorandom(0)
			ind.mutate(mutRate=0.3, mutStep=0.1)
			mutants.append(ind.mutant)

		assert all(mutants) or not any(mutants), "Mutant does not depend on seed: {0}".format(set(mutants))
		
	def test_mutants_are_drawn_from_binomial(self, pseudorandom):
		pseudorandom(0)
		self.nIndividuals = 1000
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create(n=self.nIndividuals)
		self.mutationRate = 0.2
		
		self.mutantCount = 0
		for ind in self.fakepop.individuals:
			ind.mutate(mutRate=self.mutationRate, mutStep=0.05)
			if ind.mutant:
				self.mutantCount += 1
		
		stat1, pval1 = scistats.ttest_1samp([1] * self.mutantCount + [0] * (self.nIndividuals - self.mutantCount), self.mutationRate)
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(self.mutantCount/self.nIndividuals, self.mutationRate)
		self.test = scistats.binom_test(self.mutantCount, self.nIndividuals, self.mutationRate, alternative = "two-sided")
		assert self.test > 0.05, "Success rate = {0} when mutation rate = {1}".format(self.mutantCount/self.nIndividuals, self.mutationRate)
		
		gc.collect()

	def test_deviation_depends_on_seed(self, pseudorandom):
		self.nIndividuals = 1000
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create(n=self.nIndividuals)

		mutationDeviations = []

		for ind in self.fakepop.individuals:
			pseudorandom(0)
			ind.mutate(mutRate=1, mutStep=0.05)
			mutationDeviations.append(ind.mutationDeviation)

		assert all([x == mutationDeviations[0] for x in mutationDeviations]), "Mutation deviation does not depend on seed: {0}".format(set(mutationDeviations))
		
	def test_deviation_function_returns_float(self):
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create(n=1)
		self.indiv = self.fakepop.individuals[0]
		self.v = self.indiv.vigilance
		
		for mutationBool in [True, False]:
			self.indiv.mutant = mutationBool
			self.indiv.deviate(mutStep=0.05)
			assert type(self.indiv.mutationDeviation) is float
			
		gc.collect()
		
	def test_mutants_get_deviation_from_phenotype(self):
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create(n=1)
		self.indiv = self.fakepop.individuals[0]
		self.indiv.mutate(mutRate=1,mutStep=0.05)
		assert hasattr(self.indiv, "mutationDeviation"), "Individual is a mutant: it needs to be set a deviation from phenotype"
		
		assert -1 < self.indiv.mutationDeviation < 1
			
		gc.collect()
			
	def test_only_mutants_change_phenotype(self):
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create(n=2)
		self.mutantIndivTrue = self.fakepop.individuals[0]
		self.mutantIndivFalse = self.fakepop.individuals[1]
		
		self.mutantIndivTrue.mutate(mutRate=1, mutStep=0.05)
		assert self.mutantIndivTrue.mutant, "Uh-oh, looks like the individual did not mutate when it should have..."
		assert self.mutantIndivFalse.mutationDeviation != 0, "Your mutant (bool={0}) phenotype does not deviate!".format(self.mutantIndivTrue.mutant)
		
		self.mutantIndivFalse.mutate(mutRate=0, mutStep=0.05)
		assert not self.mutantIndivFalse.mutant
		assert self.mutantIndivFalse.mutationDeviation == 0, "Phenotype deviates even though individual not a mutant!"
		
		gc.collect()
		
	def test_mutation_deviation_follows_normal_distribution(self, pseudorandom):
		pseudorandom(0)
		self.nIndividuals = 1000
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create(self.nIndividuals)
		
		self.distri = []
		for ind in self.fakepop.individuals:
			ind.mutate(mutRate=1,mutStep=0.05) 
			self.distri.append(ind.mutationDeviation)
			
		stat1, pval1 = scistats.ttest_1samp(self.distri, float(0))
		assert pval1 > 0.05, "T-test mean failed. Observed: {0}, Expected: {1}".format(mean(self.distri),0)
		stat2, pval2 = scistats.kstest(self.distri, 'norm', args=(0,0.05), N=self.nIndividuals)
		assert pval2 > 0.05, "Test for goodness of fit failed"
		stat3, pval3 = scistats.shapiro(self.distri)
		assert pval3 > 0.05, "Test of normality failed"

		gc.collect()
 
	def test_mutation_adds_deviation_to_phenotype(self):
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create(2)
		
		# WHEN THERE IS MUTATION
		self.trueMutant = self.fakepop.individuals[0]
		self.oldPhenTrueMutant = self.trueMutant.vigilance
		
		self.trueMutant.mutant = True
		self.trueMutant.deviate(mutStep=0.05)
		assert self.trueMutant.mutationDeviation != 0, "Deviation = {0}".format(self.trueMutant.mutationDeviation)
		
		self.trueMutant.applyMutation(self.trueMutant.mutationDeviation, bound = True)
		assert self.trueMutant.vigilance != self.oldPhenTrueMutant, "New:{0}, Old:{1}".format(self.trueMutant.vigilance, self.oldPhenTrueMutant)
		
		# Reset to test the whole thing together:
		self.trueMutant.vigilance = self.oldPhenTrueMutant
		self.trueMutant.mutant = None
		self.trueMutant.mutationDeviation = None
		
		self.trueMutant.mutate(mutRate=1, mutStep=0.05)
		assert type(self.oldPhenTrueMutant) is float and type(self.trueMutant.mutationDeviation) is float, "Check that both {0} and {1} are float".format(self.oldPhenTrueMutant, self.trueMutant.mutationDeviation)
		
		assert min(1, max(0, self.oldPhenTrueMutant + self.trueMutant.mutationDeviation)) == pytest.approx(self.trueMutant.vigilance), "Deviation not added to mutant phenotype: returns {0} instead of {1}!".format(self.trueMutant.vigilance, self.oldPhenTrueMutant + self.trueMutant.mutationDeviation)
		
		# WHEN THERE IS NO MUTATION
		self.falseMutant = self.fakepop.individuals[1]
		self.oldPhenFalseMutant = self.falseMutant.vigilance
		
		self.falseMutant.mutant = False
		self.falseMutant.deviate(mutStep=0.05)
		assert self.falseMutant.mutationDeviation == 0, "Deviation = {0}".format(self.falseMutant.mutationDeviation)
		
		self.falseMutant.applyMutation(self.falseMutant.mutationDeviation, bound = True)
		assert self.falseMutant.vigilance == self.oldPhenFalseMutant, "New:{0}, Old:{1}".format(self.falseMutant.vigilance, self.oldPhenFalseMutant)
		
		# Reset to test the whole thing together:
		self.falseMutant.vigilance = self.oldPhenFalseMutant
		self.falseMutant.mutant = None
		self.falseMutant.mutationDeviation = None
		
		self.falseMutant.mutate(mutRate=0, mutStep=0.05)
		assert self.oldPhenFalseMutant == self.falseMutant.vigilance, "Your individual shows mutant characteristic = {0}. Yet its phenotype deviates by {1}".format(self.falseMutant.mutant, [x-y for x, y in zip(self.falseMutant.vigilance, self.oldPhenFalseMutant)])
		assert self.oldPhenFalseMutant == self.falseMutant.vigilance, "Before: {0}, Deviation: {1}, After: {2}".format(self.oldPhenFalseMutant, self.falseMutant.mutationDeviation, self.falseMutant.vigilance)
		
		gc.collect()
		
	def test_mutation_does_not_affect_phenotype_type(self):
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.create(n=1)
		self.indiv = self.fakepop.individuals[0]
		self.phen = self.indiv.vigilance
		
		self.indiv.mutate(mutRate=1, mutStep=0.05)
		assert type(self.indiv.vigilance) is float
		
		gc.collect()

	def test_individual_mutation_can_be_unbounded(self):
		self.fakepop = Pop("test/test/parameters.txt")
		self.fakepop.nIndiv = 100
		self.fakepop.initialVigilance = 1
		self.fakepop.create()

		collectPhenotypes = []

		for ind in self.fakepop.individuals:
			ind.mutate(1,0.5,bounded = False)
			collectPhenotypes.append(ind.vigilance)

		assert any([i > 1 for i in collectPhenotypes]), "no phenotype went over 1, even when unbounded."

	# def test_population_mutation_can_be_unbounded(self):
	# 	self.pop = Pop(par='test/test/parameters.txt')
		
	# 	self.pop.numberOfDemes = 10
	# 	self.pop.initialDemeSize = 10
	# 	self.pop.mutationRate = 1
	# 	self.pop.mutationStep = 0.5
	# 	self.pop.migrationRate = 0
	# 	self.pop.initialPhenotypes

	# 	self.pop.createAndPopulateDemes()
	# 	self.pop.clearDemeInfo()
	# 	self.pop.populationMutationMigration()

	# 	collectPhenotypes = []

	# 	for ind in self.pop.individuals:
	# 		for phen in ind.phenotypicValues:
	# 			collectPhenotypes.append(phen)

	# 	assert any([i > 1 for i in collectPhenotypes]), "no phenotype went over 1, even when unbounded."

