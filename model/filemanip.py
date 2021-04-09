# -*- coding: utf-8 -*-
"""File Manipulation

Scan and extract info from files
"""

import os 

def extractColumnFromFile(fileToRead, col):
	"""Return a list
	
	Extracts data from fileToRead (comma-separated) for column col.
	Automatically detects data type (str, int, float).
	Creates a list for each line of the column.
	"""
	with open(fileToRead) as f:
		dataList = []
		for line in f.readlines():
			dat = line.rstrip().split(',')[col]
			if dat.isalpha():
				dataList.append(str(dat))
			elif dat.isdigit():
				dataList.append(int(dat))
			else:
				dataList.append(float(dat))

		return dataList