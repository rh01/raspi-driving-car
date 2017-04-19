import numpy as np
import csv

class Searcher:
  def __init__(self, index_path):
    self.index_path = index_path

  def search(self, query_features, limit = 10):
    results = {} # dictionary allows a unique ID lookup

    with open(self.index_path) as i:
      reader = csv.reader(i)

      for row in reader:
        features = [float(x) for x in row[1:]]
        d = self.chi2_dist(features, query_features)
        results[row[0]] = d

      i.close()

    results = sorted([(v, k) for (k, v) in results.items()])

    return results[:limit]

  def chi2_dist(self, hist_a, hist_b, epsilon = 1e-10):
    d = 0.5 * np.sum([((a - b) ** 2) / (a + b + epsilon) for (a, b) in zip(hist_a, hist_b)])
    return d