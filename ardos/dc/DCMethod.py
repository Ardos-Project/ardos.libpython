class DCMethod:

	def __init__(self, parent, name, data):
		self.parent = parent
		self.name = name
		self.data = data

		# Our index within a dclass.
		self.methodIndex = None

		# Method keywords.
		self.keywords = []

		# Method arguments.
		self.args = []

		# Process all the data passed to us.
		self.loadMethod()

	def loadMethod(self):
		# Load keywords.
		keywords = self.data["keywords"].split(', ')
		for keyword in keywords:
			self.keywords.append(keyword)

		# Load args.
		for arg in self.data["args"]:
			# Append the method type to our args.
			self.args.append(self.data["args"][arg])

			# Calculate the method name into the hash.
			self.parent.parent.hashGenerator.addString(arg)

		# Calculate the method data into the hash.
		for arg in self.args:
			self.parent.parent.hashGenerator.addArg(arg.split(' = ')[0])

	def hasKeyword(self, name):
		return name in self.keywords

	def getIndex(self):
		return self.methodIndex