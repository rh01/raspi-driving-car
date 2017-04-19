import numpy as np
import cv2

class Descriptor:
  def __init__(self, bins):
    self.bins = bins

  def describe(self, image):
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    features = []

    (h, w) = image.shape[:2]
    (cX, cY) = (int(w * 0.5), int(h * 0.5))

    segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]

    (xL, yL) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
    elli = np.zeros(image.shape[:2], dtype = 'uint8')
    cv2.ellipse(elli, (cX, cY), (xL, yL), 0, 0, 360, 255, -1)

    for (x0, x1, y0, y1) in segments:
      rect = np.zeros(image.shape[:2], dtype = 'uint8')
      cv2.rectangle(rect, (x0, y0), (x1, y1), 255, -1)
      rect = cv2.subtract(rect, elli)

      hist = self.histogram(image, rect)
      features.extend(hist)

    hist = self.histogram(image, elli)
    features.extend(hist)

    return features

  def histogram(self, image, mask):
    hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()

    return hist