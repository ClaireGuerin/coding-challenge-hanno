# -*- coding: utf-8 -*-
"""Ecosystem Grid

Stores information about the ecosystem status on each cell of the grid (size: dim*dim).
grid.resources are the current amount of resources in each cell.
grid.share are the individual shares of resources for each cell, SUM(1-v)/(n*gamma)
"""

import numpy as np

class Grid(object):

	def __init__(self, dim, init):
		self.initialResources = init
		self.dimension = dim

		self.resources = np.full(shape=[dim, dim], fill_value=init, dtype="float32")
		self.share = np.empty(shape=[dim, dim], dtype="float32")