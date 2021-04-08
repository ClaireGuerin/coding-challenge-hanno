import pytest
from model.individual import Individual as Ind

class TestIndividualObject(object):

	def test_individual_instance_has_vigilance_attr(self):
		self.ind = Ind(m=3)
		assert hasattr(self.ind, "vigilance"), "individual has no vigilance level"

	def test_individual_vigilance_of_right_format(self):
		self.ind = Ind(m=3)

		assert type(self.ind.vigilance) is float
		assert self.ind.vigilance >= 0.0
		assert self.ind.vigilance <= 1.0

	def test_individual_instance_has_coordinates_attr(self):
		self.ind = Ind(m=3)
		assert hasattr(self.ind, "coordinates"), "individual has no coordinates"

	def test_individual_coordinates_of_right_format(self):
		self.ind = Ind(m=3)

		assert type(self.ind.coordinates) is list
		assert len(self.ind.coordinates) == 2
		assert type(self.ind.coordinates[0]) is int
		assert type(self.ind.coordinates[1]) is int

	def test_individual_gets_initial_coord(self):
		self.ind = Ind(m=3)

		assert self.ind.coordinates != [-1,-1]
		assert self.ind.coordinates[0] >= 0
		assert self.ind.coordinates[1] >= 0

	def test_initial_coordinates_fit_on_grid(self):
		# 3*3 grid
		size = 3
		self.ind = Ind(m=size)
		assert self.ind.coordinates[0] < size
		assert self.ind.coordinates[1] < size

		# 10*10 grid
		size = 10
		self.ind = Ind(m=size)

		assert self.ind.coordinates[0] < size
		assert self.ind.coordinates[1] < size

	# def test_initial_coordinates_uniform(self):
	# 	hcoord = [-1]*100
	# 	vcoord = [-1]*100

	# 	for i in range(100):
	# 		ind = Ind()
	# 		ind.placeOnGrid(m=3)
	# 		hcoord[i] = ind.coordinates[0]
	# 		vcoord[i] = ind.coordinates[1]

