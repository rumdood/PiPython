from RgbColor import RgbColor

class ColorSequence:
	
	__current_color_index = -1
	
	def __init__(self, name=None):
		
		if name is None:
			self.name = '_internal_'
		else:
			self.name = name
			
		self.colors = []
		
	def add_color(self, color):
		self.colors.append(color)
		
	def load_from_json(self, json_object):
		if 'name' in json_object:
			self.name = json_object['name']
		
			jColors = json_object['colors']
			for color in jColors:
				self.add_color(RgbColor(color['red'], color['green'], color['blue']))
		
	def get_next_color(self):
		if (self.__current_color_index == len(self.colors) -1):
			self.__current_color_index = 0
		else:
			self.__current_color_index = self.__current_color_index + 1
			
		return self.colors[self.__current_color_index]