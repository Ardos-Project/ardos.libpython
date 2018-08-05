import struct

class NetworkWriter:

	def __init__(self, data = b''):
		self._data = data

	def getData(self):
		return self._data

	def getSize(self):
		return len(self._data)

	def addInt8(self, int8):
		self._data += struct.pack('<b', int8)

	def addUint8(self, uint8):
		self._data += struct.pack('<B', uint8)

	def addInt16(self, int16):
		self._data += struct.pack('<h', int16)

	def addUint16(self, uint16):
		self._data += struct.pack('<H', uint16)