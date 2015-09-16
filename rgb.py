import RPi.GPIO as GPIO
import time

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
	# don't let anyone set an out of bounds value
	for n, v in targetColor.items():
		if v > 100:
			targetColor[n] = 100
		elif v < 0:
			targetColor[n] = 0
		
	unmatched = set(currentColor.items()) ^ set(targetColor.items())
	if (len(unmatched) == 0): # target color has been reached
		return

	for node, value in currentColor.items():
		targetValue = targetColor[node]

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

# This is where the fun begins
ledPins = { 'Red': 17, 'Green': 22, 'Blue': 24 }
Frequency = 100

colors = setup(ledPins, Frequency)

firstColor = { 'Red': 100, 'Green': 0, 'Blue': 100 }
secondColor = { 'Red': 25, 'Green': 0, 'Blue': 75 }
thirdColor = { 'Red': 0, 'Green': 75, 'Blue': 25 }

colorSequence = [ thirdColor, secondColor, firstColor ]

colorCycleDelay = .1
colorFadeDelay = .1

try:
	color(0, 0, 0, 0) #set the initial color to all off
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