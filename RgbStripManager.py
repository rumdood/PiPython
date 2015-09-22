import time
import json
import os
import RPi.GPIO as GPIO
from ColorSequence import ColorSequence
from RgbColor import RgbColor

class RgbStripManager:
	
	def __init__(self):
		self.currentColorSequence = []
		self.azure_account_name = ''
		self.azure_account_key = ''
		self.azure_repository = []
		self.led_pins = []
		
		with open('settings.json') as settingsFile:
			settings = json.load(settingsFile)
			
			self.azure_account_key = settings["azure_account_key"]
			self.azure_account_name = settings["azure_account_name"]
			self.default_sequence = settings["default_sequence"]
			self.led_pins = { 'Red': 17, 'Green': 22, 'Blue': 24 }#settings["led_pins"]
			self.led_frequency = settings["led_frequency"]
			self.color_cycle_delay = settings["color_cycle_delay"]
			self.color_fade_delay = settings["color_fade_delay"]
				
	def try_get_default_sequence(self):
		if (self.default_sequence != ''):
			
			# check for the local file first
			def_sequence_file = self.default_sequence + '.json'
			
			if (os.path.isfile(def_sequence_file)):
				with open(def_sequence_file) as sequence_file:
					json_obj = json.load(sequence_file)
					
				self.currentColorSequence = ColorSequence('d')
				self.currentColorSequence.load_from_json(json_obj)
			else:
				if (self.azure_account_key != '' and self.azure_account_name != ''):
					self.azure_repository = rgpAzureRepository(self.azure_account_name, self.azure_account_key)
					
					if (self.default_sequence != ''):
						self.currentColorSequence = self.azure_repository.get_sequence(self.default_sequence)
			
			if (len(self.currentColorSequence.colors) > 0):
				return True
		else:
			print("No sequence file found!")
			return False
		
	def setup_gpio(self, pins, frequency):
		GPIO.setmode(GPIO.BCM)
	
		## Enable the pins tied to the LEDs
		for set_color, pin in pins.items():
			print("Enabling " + set_color + " LED on pin " + str(pin))
			GPIO.setup(pin, GPIO.OUT)
	
		colorCollection = dict()
		colorCollection['RED'] = GPIO.PWM(pins['Red'], frequency)
		colorCollection['RED'].start(0)
		colorCollection['BLUE'] = GPIO.PWM(pins['Blue'], frequency)
		colorCollection['BLUE'].start(0)
		colorCollection['GREEN'] = GPIO.PWM(pins['Green'], frequency)
		colorCollection['GREEN'].start(0)
	
		return colorCollection
		
	def fade_to_color(self, currentColor, targetColor, on_time):
		# don't let anyone set an out of bounds value
		for n, v in targetColor.items():
			if v > 100:
				targetColor[n] = 100
			elif v < 0:
				targetColor[n] = 0
			
		unmatched = set(currentColor.items()) ^ set(targetColor.items())
		if (len(unmatched) == 0): # target set_color has been reached
			return
	
		for node, value in currentColor.items():
			targetValue = targetColor[node]
	
			if value < targetValue:
				currentColor[node] = value + 1
			elif value > targetValue:
				currentColor[node] = value - 1
	
		self.set_color(currentColor['Red'], currentColor['Green'], currentColor['Blue'], on_time)
		return self.fade_to_color(currentColor, targetColor, on_time)
		
	def set_color(self, R, G, B, on_time):
		#print("Setting Colors to %s / %s / %s" % (R, G, B))
		self.colors['RED'].ChangeDutyCycle(R)
		self.colors['GREEN'].ChangeDutyCycle(G)
		self.colors['BLUE'].ChangeDutyCycle(B)
		time.sleep(on_time)
		
	def cleanUp(self):
		self.colors['RED'].stop()
		self.colors['GREEN'].stop()
		self.colors['BLUE'].stop()
		
		GPIO.cleanup()
		time.sleep(10)
		
	def run(self):
		targetColor = { 'Red': 0, 'Green': 0, 'Blue': 0 } # default starting point
		self.colors = self.setup_gpio(self.led_pins, self.led_frequency)
		
		try:
			self.set_color(0, 0, 0, 0) #set the initial set_color to all off
		
			while (True):
				currentColor = targetColor
				targetColor = self.currentColorSequence.get_next_color()
		
				print("Cycling set_color to %s %s %s" % (targetColor['Red'], targetColor['Green'], targetColor['Blue']))
		
				fade_to_color(currentColor, targetColor, self.color_fade_delay)
				time.sleep(self.color_cycle_delay)
		
		except KeyboardInterrupt:
			pass
			
		self.cleanUp()