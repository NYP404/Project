import numpy as np

class Statistics:
    def __init__(self, values):
        self.values = np.array(values, dtype=float)

    def mean(self):
        return np.mean(self.values)

    def median(self):
        return np.median(self.values)

    def minimum(self):
        return np.min(self.values)

    def maximum(self):
        return np.max(self.values)

    def standard_deviation(self):
        return np.std(self.values)
