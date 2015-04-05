import RPi.GPIO as GPIO
import time

def setup(pins):
	GPIO.setmode(GPIO.BCM)

	## Enable the pins tied to the LEDs
	for color, pin in pins.items():
		print("Enabling " + color + " LED on pin " + str(pin))
		GPIO.setup(pin, GPIO.OUT)

def Rave(pins, iterations, speed):
	print("RAVING")
	GPIO.output(pins['Red'], True)
	time.sleep(speed)

	for i in range(0, iterations):
		for color, pin in pins.items():
			pinStatus = GPIO.input(pin)
			if pinStatus > 0:
				print(color + " OFF")
				GPIO.output(pin, False)
			else:
				print(color + " ON")
				GPIO.output(pin, True)

		##print("Iteration Complete " + str(i))
		time.sleep(speed)
			

	## shut it all down
	for color, pin in pins.items():
		GPIO.output(pin, False)

ledPins = { 'Red': 24, 'Yellow': 12 }

setup(ledPins)
Rave(ledPins, 20, .25)
GPIO.cleanup()