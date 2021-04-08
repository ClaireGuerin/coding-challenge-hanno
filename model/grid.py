import numpy as np

class Grid(object):

	def __init__(self, dim):
		self.resources = np.empty(shape=[dim, dim], dtype="float32")
		self.share = np.empty(shape=[dim, dim], dtype="float32")