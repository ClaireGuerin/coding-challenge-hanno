import os 

def getPathToFile(filename, dirname=None):
	if dirname is None:
		f = filename
	else:
		f = '{0}/{1}'.format(dirname,filename)
	return "{0}/{1}".format(os.getcwd(), f)
	
def searchFile(fileToRead, string):
	with open(fileToRead) as f:
		if string in f.read():
			assert True
		else:
			assert False, "{0} not provided in {1}".format(string, fileToRead)		
	
def extractColumnFromFile(fileToRead, col):
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