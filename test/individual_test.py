import pytest
from model.individual import Individual as Ind

class TestIndividualObject(object):

	def test_individual_instance_has_vigilance_attr(self):
		self.ind = Ind()
		assert hasattr(self.ind, "vigilance"), "individual has no vigilance level"