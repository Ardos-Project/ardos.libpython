import os
import json

class DCFile:

	def __init__(self, parent, path):
		self.parent = parent
		self.path = path
		self.name = ''

		self.jsonData = None
		self.sortedClasses = []

		self.loadDCFile()

	def loadDCFile(self):
		self.name, fileExtension = os.path.splitext(self.path)

		try:
			with open(self.path, 'r') as dcFile:
				self.jsonData = json.load(dcFile)
		except:
			print("Error: Could not open DCFile '%s' at path '%s'" % (self.name, self.path))
			raise

		self.parseDCFile()

	def parseDCFile(self):
		try:
			self.loadTypeDefs()
			self.loadStructs()
			self.loadDistributedObjects()
		except:
			raise

	def loadTypeDefs(self):
		if 'typedefs' not in self.jsonData:
			# No typedefs were defined in this dc file.
			return

		for typedef in self.jsonData["typedefs"]:
			# For now, just push it straight into our typedef table.
			self.parent.addTypeDef(typedef, self.jsonData["typedefs"][typedef])

	def loadStructs(self):
		if 'structs' not in self.jsonData:
			# No structs were defined in this dc file.
			return

		for struct in self.jsonData["structs"]:
			print("struct: %s" % struct)

	def loadDistributedObjects(self):
		if 'classes' not in self.jsonData:
			# No classes were defined in this dc file.
			return

		for dclass in self.jsonData["classes"]:
			# Add the dclass as a known dclass.
			self.parent.dclasses.add(dclass)
			# We have to order the classes first before assigning them ID's.
			self.sortedClasses.append(dclass)

		# Sort the classes.
		self.sortedClasses.sort()

		for dclass in self.sortedClasses:
			self.parent.addDClass(dclass, self.jsonData["classes"][dclass])