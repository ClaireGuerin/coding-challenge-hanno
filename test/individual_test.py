import pytest
from model.individual import Individual as Ind

class TestIndividualObject(object):

	def test_individual_instance_has_vigilance_attr(self):
		self.ind = Ind()
		assert hasattr(self.ind, "vigilance"), "individual has no vigilance level"

	def test_individual_vigilance_of_right_format(self):
		self.ind = Ind()

		assert type(self.ind.vigilance) is float
		assert self.ind.vigilance >= 0.0
		assert self.ind.vigilance <= 1.0

	def test_individual_instance_has_coordinates_attr(self):
		self.ind = Ind()
		assert hasattr(self.ind, "coordinates"), "individual has no coordinates"

	def test_individual_coordinates_of_right_format(self):
		self.ind = Ind()

		assert type(self.ind.coordinates) is list
		assert len(self.ind.coordinates) == 2
		assert type(self.ind.coordinates[0]) is int
		assert type(self.ind.coordinates[1]) is int