import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT)
GPIO.output(7,0)
time.sleep(0.05)
GPIO.output(7,1)
time.sleep(0.05)

GPIO.cleanup()

