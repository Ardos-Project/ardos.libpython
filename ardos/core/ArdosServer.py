from ardos.core.MsgTypes import MsgTypes
from ardos.core.ParticipantTypes import ParticipantTypes
from ardos.net.NetworkClient import NetworkClient
from ardos.net.NetworkReader import NetworkReader
from ardos.net.NetworkWriter import NetworkWriter
from ardos.instance.InstanceObject import InstanceObject
from ardos.instance.InstanceObjectManager import InstanceObjectManager

class ArdosServer(NetworkClient):
	"""
	This is the base class for every participant of the Ardos cluster that wishes 
	to act as a game server (either as a global server or an instance server).
	This class should be configured to make a connection to a message director
	and is treated as (almost) entirely trusted.
	"""

	def __init__(self):
		super().__init__()

		self.instanceObjectManager = InstanceObjectManager(self)

		self.tempIdCount = 1
		self.tempIdMax = 4294967294 # Max uint32 size - 1

	def handleConnect(self):
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

	def generatePid(self):
		writer = NetworkWriter()

		writer.addUint16(ParticipantTypes["MESSAGE_DIRECTOR_PID"])
		writer.addUint16(MsgTypes["MESSAGE_DIRECTOR_GENERATE_PID"])

		self.send(writer)

	def subscribePid(self, pid):
		print("Got PID: " + str(pid))
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

		iObject.sendGenerateInstanceObject(self, tempId, parentId, zoneId)