import socket
# from rpiGPIO import *
import RPi.GPIO as GPIO
import time

class rpiGPIOHelper(object):
    def __init__(self):
        print "start recving command data......"
        self.__data = "pi"
        GPIO.setmode(GPIO.BOARD)

    def right(self):
        GPIO.setup(15, GPIO.OUT)
        GPIO.output(15,0)
        time.sleep(0.15)
        GPIO.output(15,1)
        print "pi car right."

    def left(self):
        GPIO.setup(13, GPIO.OUT)
        GPIO.output(13,0)
        time.sleep(0.15)
        GPIO.output(13,1)
        print "pi car left."
        
    def up(self):
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11,0)
        time.sleep(0.15)
        GPIO.output(11,1)
        print "pi car forwarding."


    def down(self):
        GPIO.setup(7, GPIO.OUT)
        GPIO.output(7,0)
        time.sleep(0.15)
        GPIO.output(7,1)
        print "pi car backward"
    
    def turnright(self):
        GPIO.setup(15, GPIO.OUT) # left
        GPIO.setup(11, GPIO.OUT) # forword

        GPIO.output(15,0)
        GPIO.output(11,0)
        time.sleep(0.10)

        GPIO.output(15,1)
        GPIO.output(11,1)
        print "pi car turnright"

    def turnleft(self):
        GPIO.setup(13, GPIO.OUT) # left
        GPIO.setup(11, GPIO.OUT) # forword

        GPIO.output(13,0)
        GPIO.output(11,0)
        time.sleep(0.10)

        GPIO.output(13,1)
        GPIO.output(11,1)
        print "pi car turnleft"

    def clean(self):
        global recv_turn
        GPIO.cleanup()
        recv_turn = False
        print "Clean Done!!!!"

# constructure class object
gpio_helper = rpiGPIOHelper()

# recv_turn

recv_turn = True

# ============socket================ #
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.24.1.126',8004))
# ============socket================ #



while recv_turn:
    data = s.recv(1024)
    print data
    if not data: continue
    func = getattr(gpio_helper,data)
    func()
    # s.sendall(data + " had recvied!")

s.close()
