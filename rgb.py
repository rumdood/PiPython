import RPi.GPIO as GPIO
import time
import math

def setup(pins, frequency):
	GPIO.setmode(GPIO.BCM)

	## Enable the pins tied to the LEDs
	for color, pin in pins.items():
		print("Enabling " + color + " LED on pin " + str(pin))
		GPIO.setup(pin, GPIO.OUT)

	colorCollection = { , }
	colorCollection['RED'] = GPIO.PWM(pins['Red'], frequency)
	colorCollection['RED'].start(0)
	colorCollection['BLUE'] = GPIO.PWM(pins['Blue'], frequency)
	colorCollection['BLUE'].start(0)
	colorCollection['GREEN'] = GPIO.PWM(pins['Green'], frequency)
	colorCollection['GREEN'].start(0)

def color(R, G, B, on_time):
	colors['RED'].ChangeDutyCycle(R)
	colors['GREEN'].ChangeDutyCycle(G)
	colors['BLUE'].ChangeDutyCycle(B)
	time.sleep(on_time)

	colors['RED'].ChangeDutyCycle(0)
	colors['GREEN'].ChangeDutyCycle(0)
	colors['BLUE'].ChangeDutyCycle(0)

def PositiveSinWave(amplitude, angle, frquency):
	#angle in degrees  
    #creates a positive sin wave between 0 and amplitude*2  
    return amplitude + (amplitude * math.sin(math.radians(angle)*frequency) )  

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

ledPins = { 'Red': 17, 'Green': 22, 'Blue': 24 }
frequency = 100

colors = setup(ledPins, frequency)

try:
	while 1:
		for i in range(0, 720, 5):
			color(PositiveSinWave(50, i, 0.5),
				PositiveSinWave(50, i, 1),
				PositiveSinWave(50, i, 2),
				0.1 )

except KeyboardInterrupt:
	pass

ledPins['Red'].stop()
ledPins['Green'].stop()
ledPins['Blue'].stop()

GPIO.cleanup()