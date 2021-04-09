import numpy as np

class Grid(object):

	def __init__(self, dim, init):
		self.initialResources = init
		self.dimension = dim

		self.resources = np.full(shape=[dim, dim], fill_value=init, dtype="float32")
		self.share = np.empty(shape=[dim, dim], dtype="float32")