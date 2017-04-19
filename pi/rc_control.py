import socket
# from rpiGPIO import *
import RPi.GPIO as GPIO
import time

left = 13
right = 15
forward = 11
reverse = 7

t = 0.03

GPIO.setmode(GPIO.BOARD)    # Numbers pins by physical location


GPIO.setup(left, GPIO.OUT)
GPIO.output(left, GPIO.HIGH)

GPIO.setup(right, GPIO.OUT)
GPIO.output(right, GPIO.HIGH)

GPIO.setup(forward, GPIO.OUT)
GPIO.output(forward, GPIO.HIGH)

GPIO.setup(reverse, GPIO.OUT)
GPIO.output(reverse, GPIO.HIGH)


class rpiGPIOHelper(object):
    def __init__(self):
        print "start recving command data......"
        self.__data = "pi"
        # GPIO.setmode(GPIO.BOARD)

    def right(self):
        GPIO.output(15,0)
        time.sleep(t)
        GPIO.output(15,1)
        print "pi car right."

    def left(self):
        GPIO.output(13,0)
        time.sleep(t)
        GPIO.output(13,1)
        print "pi car left."
        
    def up(self):
        GPIO.output(11,0)
        time.sleep(t)
        GPIO.output(11,1)
        print "pi car forwarding."


    def down(self):
        GPIO.output(7,0)
        time.sleep(t)
        GPIO.output(7,1)
        print "pi car backward"
    
    def turnright(self):

        GPIO.output(15,0)
        GPIO.output(11,0)
        time.sleep(t)

        GPIO.output(15,1)
        GPIO.output(11,1)
        print "pi car turnright"

    def turnleft(self):

        GPIO.output(13,0)
        GPIO.output(11,0)
        time.sleep(t+0.02)

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
s.connect(('172.14.1.126',8004))
# ============socket================ #



while recv_turn:
    pre_data = s.recv(1024)
    print pre_data
    data = pre_data.split('O')[0]
    if not data: continue
    func = getattr(gpio_helper,data)
    func()
    # s.sendall(data + " had recvied!")

s.close()
