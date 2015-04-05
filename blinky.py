import RPi.GPIO as GPIO
import time

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(24, GPIO.OUT)
	GPIO.setup(12, GPIO.OUT)

def Blink(pin, iterations, speed):
	for i in range(0, iterations):
		GPIO.output(pin, True)
		time.sleep(speed)
		GPIO.output(pin, False)
		time.sleep(speed)

def Rave(pins, iterations, speed):
	print("RAVING")
	GPIO.output(pins[0], True)
	time.sleep(speed)

	for i in range(0, iterations):
		for pin in pins:
			pinStatus = GPIO.input(pin)
			if pinStatus > 0:
				GPIO.output(pin, False)
			else:
				GPIO.output(pin, True)

		print("Iteration Complete " + str(i))
		time.sleep(speed)
			

	## shut it all down
	for pin in pins:
		GPIO.output(pin, False)

##redPin = 24
##redIterations = 10
##redSpeed = .5

##yellowPin = 12
##yellowIterations = 5
##yellowSpeed = .25

setup()
ledPins = [24, 12]
Rave(ledPins, 5, .25)
GPIO.cleanup()