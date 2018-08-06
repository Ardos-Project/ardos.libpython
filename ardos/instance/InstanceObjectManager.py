class InstanceObjectManager:

	def __init__(self, parent):
		self.parent = parent

		# All Instance Id's of instanced objects on this server.
		self.localInstanceIds = set()

		# Dict of {Temp Id: Instance Object}
		self.tempId2iObject = {}

		# Dict of {Instance Id: Instance Object}
		self.instanceId2iObject = {}

		# Keeps track of all instanced objects under their Parent->Zone key-pair.
		self.locationDict = {}

	def storeTempObject(self, tempId, iObject):
		if tempId in self.tempId2iObject:
			print("Warning: TempId (%s) already exists in TempId dict. Overriding." % tempId)

		self.tempId2iObject[tempId] = iObject

	def deleteTempObject(self, tempId):
		if tempId not in self.tempId2iObject:
			print("Error: Attempted to delete non-existent object with TempId (%s)" % tempId)
			return

		self.tempId2iObject.remove(tempId)

	def activateTempObject(self, tempId):
		if tempId not in self.tempId2iObject:
			print("Error: Attempted to activate non-existent TempId (%s)" % tempId)
			return

		iObject = self.tempId2iObject[tempId]

		self.storeInstanceObject(iObject)
		self.deleteTempObject(tempId)

	def storeInstanceObject(self, iObject):
		instanceId = iObject.instanceId

		if instanceId in self.localInstanceIds:
			print("Warning: Instance Object (%s) already exists in localInstanceIds. Duplicate generate or poor cleanup?" % instanceId)

		if instanceId in self.instanceId2iObject:
			print("Warning: Instance Object (%s) already exists in memory. Overriding." % instanceId)

		# Store object in memory.
		self.instanceId2iObject[instanceId] = iObject

		# Store object in location.
		parentId = iObject.parentId
		zoneId = iObject.zoneId

		parentDict = self.locationDict.setdefault(parentId, {})
		zoneDict = parentDict.setdefault(zoneId, set())
		zoneDict.add(iObject)

		# Store the instance id as a known id.
		self.localInstanceIds.add(instanceId)

	def deleteInstanceObject(self, instanceId):
		if (instanceId not in self.localInstanceIds) or (instanceId not in self.instanceId2iObject):
			print("Error: Attempted to delete invalid Instance Object (%s)" % instanceId)
			return

		iObject = self.instanceId2iObject[instanceId]

		# Get object location.
		parentId = iObject.parentId
		zoneId = iObject.zoneId

		# Remove the object from memory.
		self.instanceId2iObject.remove(instanceId)		
		self.localInstanceIds.remove(instanceId)

		parentDict = self.locationDict.get(parentId)
		if parentDict is None:
			print("Error: Attempted to delete Instance Object (%s) with invalid parent (%s)." % (instanceId, parentId))
			return

		zoneDict = parentDict.get(zoneId)
		if zoneDict is None:
			print("Error: Attempted to delete Instance Object (%s) with invalid parent-zone pair (%s:%s)." % (instanceId, parentId, zoneId))
			return

		if instanceId not in zoneDict:
			print("Error: Attempted to delete Instance Object (%s) that does not exist at location (%s:%s)." % (instanceId, parentId, zoneId))
			return

		# We can finally delete the object out of the locationDict.
		zoneDict.remove(instanceId)

		# Cleanup.
		if len(zoneDict) == 0:
			del parentDict[zoneId]
			if len(parentDict) == 0:
				del self.locationDict[parentId]

	def getInstanceObjects(self, parentId, zoneId=None):
		parent = self.locationDict.get(parentId)
		if parent is None:
			return []

		# If no zoneId is specified, return all child objects of the parent.
		if zoneId is None:
			children = []
			for zone in parent.values():
				for iObject in zone:
					children.append(iObject)

		# If we have a specific zoneId, return all objects under that zone.
		else:
			children = parent.get(zoneId, [])

		return children