class ArdosClient(NetworkClient):
	"""
	This is the base class for every participant of the Ardos cluster that wishes 
	to act as a game client. This class should be configured to make a connection
	to a client agent and is largely untrusted.
	"""

	def __init__(self):
		super().__init__()