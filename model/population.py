class Population(object):

	def __init__(self):
		pass

	def launch(self):
		with open("vigilance_out.txt", "w") as f:
			f.write('I wrote something')