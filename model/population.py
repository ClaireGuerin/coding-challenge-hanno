import model.filemanip as fman
from model.individual import Individual as Ind
from model.grid import Grid

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
		pass

	def lifeCycle(self):	
		self.pool = []
		totalVigilance = 0

		for indiv in range(self.nIndiv):
			totalVigilance += 1

			ind = self.individuals[indiv]
			res = self.grid.resources[ind.coordinates[0], ind.coordinates[1]]
			share = self.grid.share[ind.coordinates[0], ind.coordinates[1]]
			ind.gather(resources=float(res), share=share, efficiency=self.efficiency)
			ind.reproduce(fecundity=self.fecundity)
			self.pool.extend([indiv] * ind.offspring)


		self.vigilance = totalVigilance


	def launch(self):
		with open("vigilance_out.txt", "w") as f:
			for gen in range(self.nGen):
				f.write('I wrote something\n')