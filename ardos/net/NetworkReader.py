import struct

class NetworkReader:

	def __init__(self, data, index = 0):
		self._data = data
		self._index = index

	def checkReadOverflow(self, bytesToAdd):
		if (self._index + bytesToAdd > len(self._data)):
			raise Exception("Attempted to read more data than available")

	def readInt8(self):
		self.checkReadOverflow(1)
		
		read = struct.unpack('<b', self._data[self._index : self._index + 1])[0]
		self._index += 1

		return read

	def readUint8(self):
		self.checkReadOverflow(1)

		read = struct.unpack('<B', self._data[self._index : self._index + 1])[0]
		self._index += 1

		return read

	def readInt16(self):
		self.checkReadOverflow(2)

		read = struct.unpack('<h', self._data[self._index : self._index + 2])[0]
		self._index += 2

		return read

	def readUint16(self):
		self.checkReadOverflow(2)

		read = struct.unpack('<H', self._data[self._index : self._index + 2])[0]
		self._index += 2

		return read