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

	def packRequiredFields(self, distObject, writer):
		for methodName in self.dclassesByName[distObject.dclassName].methodsByName:
			method = self.dclassesByName[distObject.dclassName].methodsByName[methodName]

			# If the method isn't marked as required, skip it.
			if not method.hasKeyword("required"):
				continue

			# Pack the method id into our writer.
			writer.addUint32(method.methodIndex)

			# Pack each arg into our writer.
			# This calls the actual pythonic function within the instance class.

			# If the method is prefixed with set, change it to get.
			if (methodName[:3] == 'set'):
				methodName = 'get' + methodName[3:]

			# Otherwise, reformat our name and manually add 'get' to it.
			else:
				# Prepend 'get' to our method name.
				methodName = 'get' + methodName[:]

				# Uppercase the character preceding 'get'.
				# Purely to follow conventions.
				methodName = methodName[:3] + methodName[3].capitalize() + methodName[4:]

			# Get our value(s) from the function (or it's default as defined in the dc file).
			try:
				values = getattr(distObject, methodName)()
			except:
				print("Missing required function '%s' in '%s'" % (methodName, distObject.dclassName))
				raise

			# Are we dealing with an array or a single value?
			if isinstance(values, list):
				index = 0
				for arg in values:
					# If the value is none, get it's possible default.
					if arg == None:
						try:
							default = method.args[index].split(' = ')[1]
							values[index] = default
							index += 1
						except:
							print("Missing one or more required values in '%s' of '%s'" % (methodName, distObject.dclassName))
							return
					else:
						index += 1

			else:
				# If the value is none, get it's possible default.
				if values == None:
					try:
						default = method.args[0].split(' = ')[1]
						values = default
					except:
						print("Missing required value '%s' in '%s'" % (methodName, distObject.dclassName))
						return

			print("Method arg: %s" % values)
			print("Method name: %s" % methodName)