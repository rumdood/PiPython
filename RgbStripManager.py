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
		self.__bryan_of_nazareth = False
		
		with open('settings.json') as settingsFile:
			settings = json.load(settingsFile)
			
			self.default_sequence = settings["default_sequence"]
			self.led_pins = settings["led_pins"]
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
		colorCollection['RED'] = GPIO.PWM(pins["red"], frequency)
		colorCollection['RED'].start(0)
		colorCollection['BLUE'] = GPIO.PWM(pins["blue"], frequency)
		colorCollection['BLUE'].start(0)
		colorCollection['GREEN'] = GPIO.PWM(pins["green"], frequency)
		colorCollection['GREEN'].start(0)
	
		return colorCollection
		
	def fade_to_color(self, currentColor, targetColor, on_time):
		# don't let anyone set an out of bounds value
		if (targetColor.red > 100):
			targetColor.red = 100
		elif (targetColor.red < 0):
			targetColor.red = 0
			
		if (targetColor.green > 100):
			targetColor.green = 100
		elif (targetColor.green < 0):
			targetColor.green = 0;
		
		if (targetColor.blue > 100):
			targetColor.blue = 100
		elif (targetColor.blue < 0):
			targetColor.blue = 0
		
		if (currentColor == targetColor):
			return;
		
		# I'm sure there's a better way to do this next bit...
		if (currentColor.red < targetColor.red):
			currentColor.red = currentColor.red + 1
		elif (currentColor.red > targetColor.red):
			currentColor.red = currentColor.red - 1
		if (currentColor.green < targetColor.green):
			currentColor.green = currentColor.green + 1
		elif (currentColor.green > targetColor.green):
			currentColor.green = currentColor.green - 1
		if (currentColor.blue < targetColor.blue):
			currentColor.blue = currentColor.blue + 1
		elif (currentColor.blue > targetColor.blue):
			currentColor.blue = currentColor.blue - 1
	
		self.set_color(currentColor.red, currentColor.green, currentColor.blue, on_time)
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
		
	def enable(self):
		self.__bryan_of_nazareth = True
		
	def disable(self):
		self.__bryan_of_nazareth = False
		
	def run_color_cycles(self):
		targetColor = RgbColor(0, 0, 0) # default starting point
		currentColor = RgbColor(0, 0, 0)
		
		while (self.__bryan_of_nazareth):
			targetColor = self.currentColorSequence.get_next_color()
			#print("Cycling set_color to %s %s %s" % (targetColor.red, targetColor.green, targetColor.blue))		
			self.fade_to_color(currentColor, targetColor, self.color_fade_delay)
			time.sleep(self.color_cycle_delay)
		
	def run(self):
		self.colors = self.setup_gpio(self.led_pins, self.led_frequency)
		
		try:
			self.set_color(0, 0, 0, 0) #set the initial set_color to all off
			self.run_color_cycles()
		
		except KeyboardInterrupt:
			pass
		
		self.fade_to_color(currentColor, RgbColor(0, 0, 0), self.color_fade_delay)	
		self.cleanUp()
