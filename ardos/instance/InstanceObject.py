from ardos.core.MsgTypes import MsgTypes
from ardos.core.ParticipantTypes import ParticipantTypes
from ardos.net.NetworkReader import NetworkReader
from ardos.net.NetworkWriter import NetworkWriter

class InstanceObject:

	def __init__(self, parent):
		self.parent = parent

		self.instanceId = None
		self.parentId = None
		self.zoneId = None

	def sendGenerateInstanceObject(self, tempId, parentId, zoneId):
		self.parentId = parentId
		self.zoneId = zoneId

		writer = NetworkWriter()

		writer.addUint16(ParticipantTypes["STATE_SERVER_PID"])
		writer.addUint16(MsgTypes["STATE_SERVER_GENERATE_INSTANCE"])
		writer.addUint32(tempId)
		writer.addUint32(parentId)
		writer.addUint32(zoneId)

		# TODO: Pack required DC fields.

		self.parent.send(writer)