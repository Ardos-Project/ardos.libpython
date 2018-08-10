class DCHashGenerator:

	def __init__(self):
		# Maximum Prime Number limit.
		self.maxPrimeNumbers = 10000
		self.primes = [2]
		self.index = 0
		self.hash = 0

	def addInt(self, value):
		self.hash += self.getIndexPrime() * value
		self.index = (self.index + 1) % self.maxPrimeNumbers # Enforce our max prime limit.

	def addString(self, value):
		pass

	def getHash(self):
		return (self.hash & 0xffffffff) # uint32 hash.

	def getIndexPrime(self):
		possiblePrime = self.primes[-1] + 1 # Return the last number in our list and increase it by one.
		
		# Generate every possible prime number up to our index.
		while(len(self.primes) <= self.index):
			isPrime = True
			primeIndex = 0

			while (isPrime and (self.primes[primeIndex] * self.primes[primeIndex]) <= possiblePrime):
				# Our possible prime isn't prime if one of our primes divides it evenly.
				if ((self.primes[primeIndex] * possiblePrime / self.primes[primeIndex]) == possiblePrime):
					isPrime = False

				primeIndex += 1

			if (isPrime):
				self.primes.append(possiblePrime)

			possiblePrime += 1

		return self.primes[self.index]