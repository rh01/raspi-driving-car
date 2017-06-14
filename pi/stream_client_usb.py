"""
Reference:
PiCamera documentation
https://picamera.readthedocs.org/en/release-1.10/recipes2.html

"""

import io
import socket
import struct
import time
# import picamera
import cv2
from PIL import Image


# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('172.24.1.126', 8000))
connection = client_socket.makefile('wb')
cap = cv2.VideoCapture()
ret = cap.set(3,320)
ret = cap.set(4,240)
cap.set(15,0.2)

try:
    # with picamera.PiCamera() as camera:
    while (True):
        rc, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(imgRGB)
        start = time.time()
        stream = io.BytesIO()  # 10 frames/sec
        jpg.save(stream, 'JPEG')

        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())
        if time.time() - start > 600:
            break
        stream.seek(0)
        stream.truncate()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()

