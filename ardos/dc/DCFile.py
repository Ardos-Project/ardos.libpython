import os
import json

class DCFile:

	def __init__(self, parent, path):
		self.parent = parent
		self.path = path
		self.name = ''

		self.jsonData = None

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
			print("typedef: %s" % typedef)

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
			print("dclass: %s" % dclass)