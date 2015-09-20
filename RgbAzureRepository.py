from azure.storage.table import TableService, Entity
from RgbColor import RgbColor
from ColorSequence import ColorSequence

class RgbAzureRepository:
	"""Performs storage/retrieval functions for RGB sequences"""
	
	def __init__(self, azure_account_name, azure_account_key):
		self.table_service = TableService(account_name=azure_account_name, account_key=azure_account_key)
	
	def create_rgb_sequence_table(self):
		self.table_service.create_table('rgbsequences')

	#def add_color_to_sequence(sequenceName, red, green, blue):
	#	color = Entity()
	#	color.PartitionKey = sequenceName
	#	color.RowKey = '1'
	#	color.Red = red
	#	color.Green = green
	#	color.Blue = blue 
	#	
	#	table_service.insert_entity('rgbsequences', color)
		
	def get_sequence(self, sequence_name):
		colors = table_service.query_entities('rgbsequences', "PartitionKey eq '%s'" % sequence_name)
		
		sequence = ColorSequence(sequence_name)
		
		for color in colors:
			rgb = RgbColor(color.red, color.green, color.blue)
			sequence.add_color(rgb)		
		
		return sequence