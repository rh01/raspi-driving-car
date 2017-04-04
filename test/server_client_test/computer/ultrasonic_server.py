import threading
import SocketServer
# import cv2
import numpy as np
import math

# distance data measured by ultrasonic sensor
sensor_data = " "



class SensorDataHandler(SocketServer.BaseRequestHandler):

    data = " "

    def handle(self):
        global sensor_data
        try:
            while self.data:
                self.data = self.request.recv(1024)
                sensor_data = round(float(self.data), 1)
                #print "{} sent:".format(self.client_address[0])
                print sensor_data
        finally:
            print "Connection closed on ultrasonic sonsor thread"


class ThreadServer(object):

    def server_thread2(host, port):
        server = SocketServer.TCPServer((host, port), SensorDataHandler)
        server.serve_forever()

    distance_thread = threading.Thread(target=server_thread2, args=('172.24.1.126', 8002))
    distance_thread.start()
    

if __name__ == '__main__':
    ThreadServer()
