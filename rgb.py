import RPi.GPIO as GPIO
import time
import math

def setup(pins, frequency):
	GPIO.setmode(GPIO.BCM)

	## Enable the pins tied to the LEDs
	for color, pin in pins.items():
		print("Enabling " + color + " LED on pin " + str(pin))
		GPIO.setup(pin, GPIO.OUT)

	colorCollection = dict()
	colorCollection['RED'] = GPIO.PWM(pins['Red'], frequency)
	colorCollection['RED'].start(0)
	colorCollection['BLUE'] = GPIO.PWM(pins['Blue'], frequency)
	colorCollection['BLUE'].start(0)
	colorCollection['GREEN'] = GPIO.PWM(pins['Green'], frequency)
	colorCollection['GREEN'].start(0)

	return colorCollection

def fadeToColor(currentColor, targetColor, on_time):
	unmatched = set(currentColor.items()) ^ set(targetColor.items())
	if (len(unmatched) == 0):
		return

	for node, value in currentColor.items():
		targetValue = targetColor[node]
		if (targetValue < 0):
			targetValue = 0
		elif (targetValue > 100):
			targetValue = 100

		if value < targetValue:
			currentColor[node] = value + 1
		elif value > targetValue:
			currentColor[node] = value - 1

	color(currentColor['Red'], currentColor['Green'], currentColor['Blue'], on_time)
	return fadeToColor(currentColor, targetColor, on_time)

def color(R, G, B, on_time):
	#print("Setting Colors to %s / %s / %s" % (R, G, B))
	colors['RED'].ChangeDutyCycle(R)
	colors['GREEN'].ChangeDutyCycle(G)
	colors['BLUE'].ChangeDutyCycle(B)
	time.sleep(on_time)

	#colors['RED'].ChangeDutyCycle(0)
	#colors['GREEN'].ChangeDutyCycle(0)
	#colors['BLUE'].ChangeDutyCycle(0)

def PositiveSinWave(amplitude, angle, frequency):
	#angle in degrees  
    #creates a positive sin wave between 0 and amplitude*2  
    return amplitude + (amplitude * math.sin(math.radians(angle)*frequency))

ledPins = { 'Red': 17, 'Green': 22, 'Blue': 24 }
Frequency = 100

colors = setup(ledPins, Frequency)

initialColor = { 'Red': 0, 'Green': 0, 'Blue': 0 }
firstColor = { 'Red': 100, 'Green': 0, 'Blue': 100 }
secondColor = { 'Red': 25, 'Green': 0, 'Blue': 75 }
thirdColor = { 'Red': 0, 'Green': 75, 'Blue': 25 }

colorSequence = [ thirdColor, secondColor, firstColor ]

colorCycleDelay = .1
colorFadeDelay = .1

try:
	color(0, 0, 0, 0) #set the initial color
	targetColor = initialColor

	while (True):
		currentColor = targetColor
		targetColor = colorSequence.pop()

		print("Cycling color to %s %s %s" % (targetColor['Red'], targetColor['Green'], targetColor['Blue']))

		colorSequence.insert(0, currentColor)

		fadeToColor(currentColor, targetColor, colorFadeDelay)
		time.sleep(colorCycleDelay)

except KeyboardInterrupt:
	pass

colors['RED'].stop()
colors['GREEN'].stop()
colors['BLUE'].stop()

GPIO.cleanup()
