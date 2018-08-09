from ardos.dc.DCFile import DCFile

class DCManager:
	"""
	The DCManager class is the root manager for each DCFile that is loaded.
	This class contains the combined hash, classes, methods, etc, of each file.
	Make sure when loding multiple DC files, that they are loaded in order of
	inheritance.
	"""

	def __init__(self):
		pass

	def loadDCFile(self, path):
		dc = DCFile(self, path)