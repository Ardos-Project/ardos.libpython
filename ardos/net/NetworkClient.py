import asyncore
import socket
import threading

from ardos.net.NetworkReader import NetworkReader
from ardos.net.NetworkWriter import NetworkWriter

class NetworkClient(asyncore.dispatcher):
	"""
	Base class utilized by both ArdosServer and ArdosClient to make an
	arbitrary connection to either a message director or client agent.
	"""

	def __init__(self):
		asyncore.dispatcher.__init__(self)

		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.buffer = bytes()

		self.thread = threading.Thread(target=asyncore.loop, kwargs={'timeout':1})
		self.thread.daemon = True
		self.thread.start()

	def send(self, writer):
		super().send(writer.getData())

	def handle_connect(self):
		self.handleConnect()

	def handle_close(self):
		self.close()

	def handle_read(self):
		data = self.recv(1024)
		reader = NetworkReader(data)
		self.handleData(reader)

	def writable(self):
		if not self.connected:
			return True

		return (len(self.buffer) > 0)

	def handle_write(self):
		sent = super().send(self.buffer)
		self.buffer = self.buffer[sent:]

	"""
	Overridden by inheritors.
	"""

	def handleConnect(self):
		pass

	def handleData(self, reader):
		pass