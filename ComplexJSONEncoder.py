from json import JSONEncoder

class ComplexJSONEncoder(JSONEncoder):
	
	def default(self, o):
		return o.__dict__
			