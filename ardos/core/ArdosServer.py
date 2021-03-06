from ardos.core.MsgTypes import MsgTypes
from ardos.core.ParticipantTypes import ParticipantTypes
from ardos.net.NetworkClient import NetworkClient
from ardos.net.NetworkReader import NetworkReader
from ardos.net.NetworkWriter import NetworkWriter
from ardos.instance.InstanceObject import InstanceObject
from ardos.dc.DCManager import DCManager
from ardos.instance.InstanceObjectManager import InstanceObjectManager

class ArdosServer(NetworkClient):
	"""
	This is the base class for every participant of the Ardos cluster that wishes 
	to act as a game server (either as a global server or an instance server).
	This class should be configured to make a connection to a message director
	and is treated as (almost) entirely trusted.
	"""

	def __init__(self):
		NetworkClient.__init__(self)

		self.pid = None

		self.dcManager = DCManager()
		self.instanceObjectManager = InstanceObjectManager(self)

		self.tempIdCount = 1
		self.tempIdMax = 0xffffffff # Max uint32 size.

	def handle_connect(self):
		self.generatePid()

	def allocateTempId(self):
		if (self.tempIdCount + 1 > self.tempIdMax):
			print("Error: Max temp id allocation reached!")
			self.tempIdCount = 1
			return self.tempIdCount

		tempId = self.tempIdCount
		self.tempIdCount += 1

		return tempId

	def handleData(self, reader):
		msgType = reader.readUint16()

		if (msgType == MsgTypes["MESSAGE_DIRECTOR_GENERATE_PID_RESP"]):
			pid = reader.readUint16()
			self.subscribePid(pid)
			self.handleConnect()

		elif (msgType == MsgTypes["STATE_SERVER_GENERATE_INSTANCE_RESP"]):
			self.handleGenerateInstanceObjectResp(reader)

	def generatePid(self):
		writer = NetworkWriter()

		writer.addUint16(ParticipantTypes["MESSAGE_DIRECTOR_PID"])
		writer.addUint16(MsgTypes["MESSAGE_DIRECTOR_GENERATE_PID"])

		self.send(writer)

	def subscribePid(self, pid):
		self.pid = pid

		writer = NetworkWriter()

		writer.addUint16(ParticipantTypes["MESSAGE_DIRECTOR_PID"])
		writer.addUint16(MsgTypes["MESSAGE_DIRECTOR_SUBSCRIBE_PID"])
		writer.addUint16(pid)

		self.send(writer)

	def generateInstanceObject(self, iObject, parentId, zoneId):
		# While the object is generating on the State Server, store it in temp memory.
		# If the object failes to generate, it is deleted out of this memory.
		# If it successfully generates, it is put into instance object memory.
		tempId = self.allocateTempId()
		self.instanceObjectManager.storeTempObject(tempId, iObject)

		# Set ParentId and ZoneId.
		iObject.parentId = parentId
		iObject.zoneId = zoneId

		iObject.sendGenerateInstanceObject(tempId)

	def handleGenerateInstanceObjectResp(self, reader):
		# Were we successful in generating the instance object?
		success = reader.readUint8()
		tempId = reader.readUint32()

		# If the state server accepted the generate, activate the temp object.
		if (success):
			instanceId = reader.readUint32()
			self.instanceObjectManager.activateTempObject(tempId, instanceId)

		# Otherwise, clear it out of memory.
		else:
			self.instanceObjectManager.deleteTempObject(tempId)