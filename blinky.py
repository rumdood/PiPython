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
	pinStatus = GPIO.input(24)
	print("24 Status: " + str(pinStatus))
	GPIO.output(pins[0], True)
	time.sleep(speed)

	for i in range(1, iterations):
		print("Iteration " + str(i))
		for pin in pins:
			print(GPIO.input(pin))

	GPIO.output(pins[0], False)

##redPin = 24
##redIterations = 10
##redSpeed = .5

##yellowPin = 12
##yellowIterations = 5
##yellowSpeed = .25

setup()
ledPins = [24, 12]
Rave(ledPins, 1, 1)
GPIO.cleanup()