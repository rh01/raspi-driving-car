import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.OUT) # left
GPIO.setup(11, GPIO.OUT) # forword

GPIO.output(13,0)
GPIO.output(11,0)
time.sleep(1)

GPIO.output(13,1)
GPIO.output(11,1)
time.sleep(0.05)

GPIO.cleanup()

