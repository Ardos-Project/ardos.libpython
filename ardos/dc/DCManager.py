from ardos.dc.DCHashGenerator import DCHashGenerator
from ardos.dc.DCFile import DCFile

class DCManager:
	"""
	The DCManager class is the root manager for each DCFile that is loaded.
	This class contains the combined hash, classes, methods, etc, of each file.
	Make sure when loding multiple DC files, that they are loaded in order of
	inheritance.
	"""

	def __init__(self):
		# Hash Generator.
		self.hashGenerator = DCHashGenerator()

		# Known dclass's. Helps with inheritance.
		self.dclasses = set()

		# Dict of {TypeDef Identifier: TypeDef Value}
		self.typedefs = {}

	def loadDCFile(self, path):
		dc = DCFile(self, path)

	def addTypeDef(self, name, value):
		if name in self.typedefs:
			# Duplicate typedefs are okay, as long as we have the same value.
			if value != self.typedefs[name]:
				print("Error: Duplicate typedef '%s' with different values '%s and %s'" % (name, self.typedefs[name], value))
				return

		self.typedefs[name] = value
		
	def addDClass(self, name, data):
		print("New DClass %s - %s" % (name, data))