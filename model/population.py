import model.filemanip as fman
from model.individual import Individual as Ind
from model.grid import Grid
import numpy as np
import random as rd

class Population(object):

	def __init__(self, par="parameters.txt"):
		attrs = fman.extractColumnFromFile(par, 0)
		vals = fman.extractColumnFromFile(par, 1)
		for attr,val in zip(attrs, vals):
			setattr(self, attr, val)

	def create(self, n=None):
		if n == None:
			n = self.nIndiv

		self.individuals = [Ind(m=self.gridSize)]*n
		self.grid = Grid(dim=self.gridSize, init=self.initRes)

	def explore(self):
		self.ncell = np.zeros([self.gridSize, self.gridSize])
		self.vcell = np.zeros([self.gridSize, self.gridSize])

		for ind in self.individuals:
			if ind.alive == False:
				continue
			else:
				ind.explore()
				self.ncell[ind.coordinates[0], ind.coordinates[1]] += 1
				self.vcell[ind.coordinates[0], ind.coordinates[1]] += 1 - ind.vigilance

	def gatherAndSurvive(self):

		for ind in self.individuals:
			res = self.grid.resources[ind.coordinates[0], ind.coordinates[1]]
			share = self.grid.share[ind.coordinates[0], ind.coordinates[1]]

			ind.gather(resources=float(res), share=share, efficiency=self.efficiency)
			ind.survive(p = self.predation)

	def routine(self):

		self.explore()

		# share in a cell S = SUM(1-v_i)/(gamma*n)
		# where gamma is the competition parameter
		# WARNING: some of the cells might be unoccupied, leading to a division by zero in our case.
		# here, divisions by zero are treated as zeroes
		divider = self.ncell * self.competition
		shares = np.true_divide(self.vcell, divider, out=np.zeros_like(self.vcell), where=divider!=0)
		self.grid.share = shares
		self.gatherAndSurvive()

		# resources in a cell deprecate as individuals share them
		# R * (1 - alpha * S) * r
		# where alpha is the efficiency of resource extraction
		# where r is the natural growth rate of resources
		# where S is the shares as calculated previously
		resourceGrowth = self.grid.resources * self.growth
		resourceConsumption = 1 - self.efficiency * shares
		self.grid.resources = resourceGrowth * resourceConsumption

	def reproduce(self):
		#parent = range(self.nIndiv)
		offspring = []

		for ind in self.individuals:
			#assert hasattr(ind, "offspring") == False

			ind.reproduce(fecundity=self.fecundity)
			offspring.append(ind.offspring)
			assert offspring[-1] == ind.offspring, "wrong order in offspring number"

		self.nextGeneration = rd.choices(population=range(self.nIndiv),
			weights=offspring,
			k=self.nIndiv)

	def update(self):

		tmpIndividuals = [Ind(m=self.gridSize)] * self.nIndiv
		self.totalVigilance = 0
		
		for offspring in range(self.nIndiv):
			ind = tmpIndividuals[offspring]
			parent = self.individuals[self.nextGeneration[offspring]]
			setattr(ind, "vigilance", parent.vigilance)
			setattr(ind, "coordinates", parent.coordinates)

			ind.mutate(mutRate=self.mutRate, mutStep=self.mutStep)

			self.totalVigilance += ind.vigilance

		self.individuals = tmpIndividuals
		self.vigilance = self.totalVigilance / self.nIndiv

	def lifeCycle(self):	

		for steps in self.routineSteps:
			self.routine()

		self.reproduce()
		self.update()


	def launch(self):
		with open("vigilance_out.txt", "w") as f:
			for gen in range(self.nGen):
				f.write('I wrote something\n')