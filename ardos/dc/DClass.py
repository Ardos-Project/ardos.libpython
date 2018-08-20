from ardos.dc.DCMethod import DCMethod

class DClass:

	def __init__(self, parent, name, data):
		self.parent = parent
		self.name = name
		self.data = data

		# Set by DCManager.
		self.dclassIndex = None

		# Method Index.
		self.methodIndex = 1

		self.sortedMethods = []

		# Dict of {Method Name: DCMethod Object}
		self.methodsByName = {}

		# Dict of {Method Id: DCMethod Object}
		self.methodsById = {}

		# Load our methods into memory.
		self.loadMethods()

	def loadMethods(self):
		# We might not have any methods defined due to inheritance.
		if 'methods' not in self.data:
			return

		# Generate each DCMethod.
		for method in self.data["methods"]:
			try:
				dcMethod = DCMethod(self, method, self.data["methods"][method])
				self.methodsByName[method] = dcMethod
			except Exception as e:
				print("Error: Could not generate DCMethod '%s'. %s" % (method, e))
				return

		# Sort our methods.
		for method in self.methodsByName:
			self.sortedMethods.append(method)

		self.sortedMethods.sort()

		# Allocate Id's for each method.
		for method in self.sortedMethods:
			self.methodsById[self.methodIndex] = self.methodsByName[method]
			self.methodsById[self.methodIndex].methodIndex = self.methodIndex
			self.methodIndex += 1

		print("DCMethods By Name: %s" % self.methodsByName)

	def loadInheritedMethods(self):
		# Insert the methods of the inherited class into our methods.
		for method in self.parent.dclassesByName[self.name].methodsByName:
			# Make sure we're not overriding a method.
			if method in self.methodsByName:
				continue

			self.methodsByName[method] = None

		# Methods in external class should already be sorted for Id allocation.
		for method in self.parent.dclassesByName[self.name].sortedMethods:
			# Make sure we're not overriding a method.
			if method in self.methodsByName:
				continue

			self.methodsById[self.methodIndex] = method
			self.methodIndex += 1