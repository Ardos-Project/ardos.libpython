class DCHashGenerator:

	def __init__(self):
		self.maxHashSize = 4294967295 # Maximum hash size (uint32)
		self.maxPrimeNumbers = 10000 # Maximum prime number limit.
		self.primes = [2]
		self.hash = 0
		self.index = 0

	def addInt(self, value):
		self.hash = (self.hash + (self.getIndexPrime() * value)) % self.maxHashSize # Enforce our max hash size.
		self.index = (self.index + 1) % self.maxPrimeNumbers # Enforce our max prime limit.

	def addString(self, value):
		self.addInt(len(value))
		chars = list(value)
		for char in chars:
			self.addInt(ord(char))

	def addArg(self, arg):
		pass

	def getHash(self):
		return (self.hash & 0xffffffff) # uint32 hash.

	def getIndexPrime(self):
		# TODO
		return self.index