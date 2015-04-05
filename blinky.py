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

redPin = 24
redIterations = 10
redSpeed = .5

yellowPin = 12
yellowIterations = 5
yellowSpeed = .25

setup()
Blink(redPin, redIterations, redSpeed)
Blink(yellowPin, yellowIterations, yellowSpeed)

GPIO.cleanup()