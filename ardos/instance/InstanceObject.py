from ardos.core.MsgTypes import MsgTypes
from ardos.core.ParticipantTypes import ParticipantTypes
from ardos.net.NetworkReader import NetworkReader
from ardos.net.NetworkWriter import NetworkWriter

class InstanceObject:

	def __init__(self):
		self.parentId = None
		self.zoneId = None
		self.instanceId = None

	def sendGenerateInstanceObject(self, tempId, parentId, zoneId):
		pass