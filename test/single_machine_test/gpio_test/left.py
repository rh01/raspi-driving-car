import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.OUT)
GPIO.output(13,0)
time.sleep(0.05)
GPIO.output(13,1)
time.sleep(0.05)

GPIO.cleanup()

