from ardos.dc.DCHashGenerator import DCHashGenerator
from ardos.dc.DCFile import DCFile
from ardos.dc.DClass import DClass

class DCManager:
	"""
	The DCManager class is the root manager for each DCFile that is loaded.
	This class contains the combined hash, classes, methods, etc, of each file.
	Make sure when loding multiple DC files, that they are loaded in order of
	inheritance.
	"""

	def __init__(self):
		#DClass index.
		self.dclassIndex = 1

		# Hash Generator.
		self.hashGenerator = DCHashGenerator()

		# Known dclass's. Helps with inheritance.
		self.dclasses = set()

		# Dict of {TypeDef Identifier: TypeDef Value}
		self.typedefs = {}

		# Dict of {DClass Name: DClass Object}
		self.dclassesByName = {}

		# Dict of {DClass Id: DClass Object}
		self.dclassesById = {}

	def loadDCFile(self, path):
		DCFile(self, path)

	def addTypeDef(self, name, value):
		if name in self.typedefs:
			# Duplicate typedefs are okay, as long as we have the same value.
			if value != self.typedefs[name]:
				print("Error: Duplicate typedef '%s' with different values '%s and %s'" % (name, self.typedefs[name], value))
				return

		self.typedefs[name] = value
		
	def addDClass(self, name, data):
		# If we have inheritance that isn't in our list of all dclasses, the class doesn't exist.
		# NOTE: This will trigger if you don't load dc files in the right order.
		# TODO: Multi-inheritance.
		if 'inherits' in data:
			if data["inherits"] not in self.dclasses:
				print("Error: Could not generate DClass '%s'. Missing inheritance '%s'" % (name, data["inherits"]))
				return

		# Make sure this DClass doesn't already exist in memory.
		# NOTE: This will most likely trigger if you have duplicate class names across dc files.
		if name in self.dclassesByName:
			print("Error: Could not generate DClass '%s'. It has already been defined")
			return

		# Attempt to generate the DClass.
		try:
			dclass = DClass(self, name, data)
		except Exception as e:
			print("Error: Could not generate DClass '%s'. %s" % (name, e))
			return

		dclass.dclassIndex = self.dclassIndex

		# Calculate the dclass name into the hash.
		self.hashGenerator.addString(name)

		# Store the DClass in memory.
		self.dclassesByName[name] = dclass
		self.dclassesById[self.dclassIndex] = dclass

		self.dclassIndex += 1

		print("Dclasses By Name: %s" % self.dclassesByName)