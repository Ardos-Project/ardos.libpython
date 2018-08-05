from ardos.core.MsgTypes import MsgTypes
from ardos.core.ParticipantTypes import ParticipantTypes
from ardos.net.NetworkClient import NetworkClient
from ardos.net.NetworkReader import NetworkReader
from ardos.net.NetworkWriter import NetworkWriter

class ArdosServer(NetworkClient):
	"""
	This is the base class for every participant of the Ardos cluster that wishes 
	to act as a game server (either as a global server or an instance server).
	This class should be configured to make a connection to a message director
	and is treated as (almost) entirely trusted.
	"""

	def __init__(self):
		super().__init__()

	def handleConnect(self):
		self.generatePid()

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