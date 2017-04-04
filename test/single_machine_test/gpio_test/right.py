import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(15, GPIO.OUT)
GPIO.output(15,0)
time.sleep(0.05)
GPIO.output(15,1)
time.sleep(0.05)

GPIO.cleanup()

