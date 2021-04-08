import model.filemanip as fman
from model.individual import Individual as Ind

class Population(object):

	def __init__(self, par="parameters.txt"):
		attrs = fman.extractColumnFromFile(par, 0)
		vals = fman.extractColumnFromFile(par, 1)
		for attr,val in zip(attrs, vals):
			setattr(self, attr, val)

	def create(self, n):
		self.individuals = [Ind()]*n

	def lifeCycle(self):	
		self.pool = []

		for ind in self.individuals:
			ind.gather(resources=None, share=None, efficiency=self.efficiency)
			ind.reproduce(fecundity=self.fecundity)


	def launch(self):
		with open("vigilance_out.txt", "w") as f:
			for gen in range(self.nGen):
				f.write('I wrote something\n')