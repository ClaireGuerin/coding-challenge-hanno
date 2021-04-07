import pytest
from model.population import Population as Pop
import random as rd
import numpy.random as np
import os

@pytest.fixture
def pseudorandom():
	def _foo(n):
		rd.seed(n)
		np.seed(n)

	return _foo

@pytest.fixture
def objectAttributesExist():
	def _foo(obj, attrs):
		tests = []
		for attr in attrs:
			tests.append(hasattr(obj, attr))
		thereIsNoProblem = all(tests)
		if thereIsNoProblem:
			result = None
		else:
			problemIndices = [i for i, x in enumerate(tests) if x == False]
			problemAttr = [attrs[a] for a in problemIndices]
			result = problemAttr	
		
		return (thereIsNoProblem, result)
	
	return _foo

@pytest.fixture
def objectAttributesValues():
	def _foo(obj, attrs, vals):
		tests = []
		values = []
		for attr,val in zip(attrs, vals):
			tests.append(getattr(obj, attr) == val)
			values.append(getattr(obj, attr))
		thereIsNoProblem = all(tests)
		if thereIsNoProblem:
			attributes = None
			expected = None
			observed = None
		else:
			indices = [i for i, x in enumerate(tests) if x == False]
			attributes = [attrs[a] for a in problemIndices]
			expected = [vals[a] for a in problemIndices]
			observed = [values[a] for a in problemIndices]
		
		return (thereIsNoProblem, attributes, expected, observed)
	
	return _foo

@pytest.fixture
def objectAttributesAreNotNone():
	def _foo(obj, attrs):
		tests = []
		for attr in attrs:
			tests.append(getattr(obj, attr) is not None)
		thereIsNoProblem = all(tests)
		if thereIsNoProblem:
			attributes = None
		else:
			indices = [i for i, x in enumerate(tests) if x == False]
			attributes = [attrs[a] for a in problemIndices]
		
		return (thereIsNoProblem, attributes)
	
	return _foo

@pytest.fixture
def clearOutputFiles():
	os.remove('vigilance_out.txt')