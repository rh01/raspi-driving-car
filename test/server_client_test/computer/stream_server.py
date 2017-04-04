import threading
import SocketServer
import cv2
import numpy as np


class VideoStreamHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        stream_bytes = ' '
        
        # stream video frames one by one
        try:
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last+2]
                    stream_bytes = stream_bytes[last+2:]
                    # cv2.CV_LOAD_IMAGE_GRAYSCALE --> 0
                    # cv2.CV_LOAD_IMAGE_UNCHANGED --> -1
                    gray = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 0)
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), -1)

                    # lower half of the image
                    half_gray = gray[120:240, :]

                    cv2.imshow('image', image)
                    #cv2.imshow('mlp_image', half_gray)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            cv2.destroyAllWindows()

        finally:
            print "Connection closed on stream thread"


class ThreadServer(object):

    def server_thread(host, port):
        server = SocketServer.TCPServer((host, port), VideoStreamHandler)
        server.serve_forever()

    
    video_thread = threading.Thread(target=server_thread('172.24.1.126', 8000))
    video_thread.start()

if __name__ == '__main__':
    ThreadServer()
