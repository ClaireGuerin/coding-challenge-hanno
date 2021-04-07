import model.filemanip as fman

class Population(object):

	def __init__(self, par="parameters.txt"):
		attrs = fman.extractColumnFromFile(par, 0, str)
		vals = fman.extractColumnFromFile(par, 1, int)
		for attr,val in zip(attrs, vals):
			setattr(self, attr, val)


	def launch(self):
		with open("vigilance_out.txt", "w") as f:
			for gen in range(self.nGen):
				f.write('I wrote something\n')