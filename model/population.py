# -*- coding: utf-8 -*-
""" Prey population

Stores and updates all individuals in the population as Individual class objects, as well as ecosystem information in a Grid class object.
Simulate life cycle over multiple generations.
"""

import model.filemanip as fman
from model.individual import Individual as Ind
from model.grid import Grid
import numpy as np
import random as rd
import logging
import os
import itertools as it

class Population(object):

	def __init__(self, par="parameters.txt", v=0.5):
		""" Initialize population by extracting parameter values from file and assigning them to self.
		"""
		logging.basicConfig(level=logging.INFO,
							format='[%(asctime)s]::%(levelname)s  %(message)s',
							datefmt='%Y.%m.%d - %H:%M:%S')

		logging.info('Population created')

		attrs = fman.extractColumnFromFile(par, 0)
		vals = fman.extractColumnFromFile(par, 1)
		for attr,val in zip(attrs, vals):
			setattr(self, attr, val)
		self.v = v # initial vigilance level can be given by user

	def create(self, n=None):
		""" Create the population.
		Return nothing
		Create n Individual prey instances and store in self.individuals
		Create ecosystem Grid instance and store in self.grid.
		"""
		if n == None:
			n = self.nIndiv

		self.deathCount = 0 # everyone is alive at the beginning of the simulation
		self.ecoTime = 0 # ecological time set to zero at beginning of simulation
		self.ecologyShortHistory = np.empty([0, 4])
		self.explorationShortHistory = np.empty([0, 4])

		self.grid = Grid(dim=self.gridSize, init=self.initRes)
		self.individuals = []
		for i in range(n):
			self.individuals.append(Ind(m=self.gridSize, v=self.v))

	def explore(self):
		""" Loop over all live individuals in the population and make them move on the ecoystem grid.
		Return nothing
		Update individual instance's coordinates
		Create self.ncell matrix of grid dimensions to store information on the number of individual in each grid cell
		Create self.vcell matrix of grid dimensions to store information on the vigilance level in each cell.
		"""
		self.ncell = np.zeros([self.gridSize, self.gridSize])
		self.vcell = np.zeros([self.gridSize, self.gridSize])


		for ind in self.individuals:
			if ind.alive == False:
				continue
			else:
				ind.explore()
				self.ncell[ind.coordinates[0], ind.coordinates[1]] += 1
				self.vcell[ind.coordinates[0], ind.coordinates[1]] += 1 - ind.vigilance
				exploration = np.array([[self.ecoTime, ind.coordinates[0], ind.coordinates[1], ind.vigilance]])
				addExploration = np.concatenate((self.explorationShortHistory, exploration))
				self.explorationShortHistory = addExploration

	def gatherAndSurvive(self):
		""" Loop over all live individuals in the population and make them gather resources and survive.
		Return nothing
		Update individual instance's storage value
		Update individual instance's alive value
		"""
		for ind in self.individuals:
			if ind.alive == False:
				continue
			else:
				res = self.grid.resources[ind.coordinates[0], ind.coordinates[1]]
				share = self.grid.share[ind.coordinates[0], ind.coordinates[1]]

				ind.gather(resources=float(res), share=share, efficiency=self.efficiency)
				ind.survive(p = self.predation)

	def routine(self):
		""" Uses explore() and gatherAndSurvive() methods to implement full routine of a single time step.
		Return nothing
		Update self.ecoTime: increment ecological time by 1 unit
		Update self.grid.share: resource share in each cell on the grid after exploration and before gathering
		Update self.grid.resources: update amount of resources in each cell on the grid after gathering.
		"""
		self.ecoTime += 1

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
		newResources = resourceGrowth * resourceConsumption
		newResources[newResources > (200 / self.fecundity)] = self.initRes # resources crash when there's too much of it in a cell, and go back to initial amount.

		tmpEcologyHistory = np.empty([self.gridSize * self.gridSize, 4])

		pos = 0
		for cell in it.product(range(self.gridSize), repeat=2):
			tmpEcologyHistory[pos,0] = self.ecoTime
			tmpEcologyHistory[pos,1] = cell[0]
			tmpEcologyHistory[pos,2] = cell[1]
			tmpEcologyHistory[pos,3] = newResources[cell[0], cell[1]]
			pos += 1

		addEcologicalHistory = np.concatenate((self.ecologyShortHistory, tmpEcologyHistory))
		self.ecologyShortHistory = addEcologicalHistory

		self.grid.resources = newResources
		assert type(self.grid.resources) == np.ndarray

	def reproduce(self):
		""" Loop over all live individuals in the population and make them reproduce.
		Return nothing
		Create offspring pool and draw nIndiv individuals from it for the next generation.
		Count the number of dead in the population.
		"""
		offspring = []

		for ind in self.individuals:
			if ind.alive == False:
				self.deathCount += 1
				offspring.append(0)
			else:
				ind.reproduce(fecundity=self.fecundity)
				offspring.append(ind.offspring)
				assert offspring[-1] == ind.offspring, "wrong order in offspring number"

		try:
			assert sum(offspring) > 0, "No offspring produced"
			self.nextGeneration = rd.choices(population=range(self.nIndiv),
											 weights=offspring,
											 k=self.nIndiv)
		except AssertionError as e:
			self.deathCount = self.nIndiv
			print(e)

	def update(self):
		""" Update population
		Return nothing
		Create new individual instances for the new generation, who inherit their parent's vigilance level and coordinates on the grid.
		Mutate individual vigilance phenotype.
		Calculate mean vigilance in the population and store it in self.vigilance.
		"""
		tmpIndividuals = []
		self.totalVigilance = 0
		
		for offspring in range(self.nIndiv):
			ind = Ind(m=self.gridSize)
			parent = self.individuals[self.nextGeneration[offspring]]
			setattr(ind, "vigilance", parent.vigilance)
			setattr(ind, "coordinates", parent.coordinates)

			ind.mutate(mutRate=self.mutRate, mutStep=self.mutStep)
			tmpIndividuals.append(ind)

			self.totalVigilance += ind.vigilance

		self.individuals = tmpIndividuals
		self.vigilance = self.totalVigilance / self.nIndiv

	def lifeCycle(self):	
		""" Full life cycle over one generation.
		Run the routine for self.routineSteps number of steps.
		Reproduce individuals and update population.
		"""
		self.ecologyShortHistory = np.empty([0, 4]) # reset ecology history for new cycle
		self.explorationShortHistory = np.empty([0, 4]) # reset ecology history for new cycle

		for steps in range(self.routineSteps):
			self.routine()

		self.reproduce()
		self.update()

	def launch(self, dev="off"):
		""" Launch a full simulation over self.nGen generations.
		Write out mean vigilance level over generation time in "vigilance.txt" file
		Interrupt simulation if population extinct (self.deathCount = 0).
		"""
		if not os.path.exists('output'):
			os.makedirs('output')

		with open("output/vigilance_out.txt", "w", buffering=1) as vigilanceFile, \
			open("output/resources_out.txt", "w", buffering=1) as resourcesFile, \
			open("output/exploration_out.txt", "w", buffering=1) as explorationFile:

			for gen in range(self.nGen):
				self.lifeCycle()
				vigilanceFile.write('{0}\n'.format(round(self.vigilance, 3)))
				np.savetxt(resourcesFile, self.ecologyShortHistory, fmt='%1.3f')
				np.savetxt(explorationFile, self.explorationShortHistory, fmt='%1.3f')

				if self.deathCount == self.nIndiv:
					logging.info('Population extinct at generation {}'.format(gen))
					break
				else:
					self.deathCount = 0

		logging.info('End of simulation')

		if dev=="on":
			logging.info('Creating visuals...')
			os.system("Rscript anim-vigil/animate_sim.r")
			os.system("xdg-open output/vigilance_out.gif")
			os.system("xdg-open output/grid_out.gif")


					