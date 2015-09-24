class RgbColor(object):
	
	def __init__(self, red, green, blue):
		self.red = red
		self.green = green
		self.blue = blue
	
	def __eq__(self, other): 
        	return self.__dict__ == other.__dict__
