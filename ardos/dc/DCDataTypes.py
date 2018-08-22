class DCDataTypes:

	def __init__(self):
		pass

	def packArg(self, writer, argType, value):
		if (argType == 'uint32'):
			writer.addUint32(int(value))
		else:
			print("Error: Invalid argType '%s'" % argType)