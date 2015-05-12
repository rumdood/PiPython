import RPi.GPIO as GPIO
import time
import math

def setup(pins):
	GPIO.setmode(GPIO.BCM)

	## Enable the pins tied to the LEDs
	for color, pin in pins.items():
		print("Enabling " + color + " LED on pin " + str(pin))
		GPIO.setup(pin, GPIO.OUT)

def color(R, G, B, on_time):
	pins['Red'].ChangeDutyCycle(R)
	pins['Green'].ChangeDutyCycle(G)
	pins['Blue'].ChangeDutyCycle(B)
	time.sleep(on_time)

	pins['Red'].ChangeDutyCycle(0)
	pins['Green'].ChangeDutyCycle(0)
	pins['Blue'].ChangeDutyCycle(0)

def PositiveSinWave(aplitude, angle, frquency):
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
frequency = 0.1

setup(ledPins)

try:
	while true:
		for i in range(0, 720, 5):
			color(PositiveSinWave(50, i, 0.5),
				PositiveSinWave(50, i, 1),
				PositiveSinWave(50, i, 2),
				frequency )

except KeyboardInterrupt:
	pass

pins['Red'].stop()
pins['Green'].stop()
pins['Blue'].stop()

GPIO.cleanup()