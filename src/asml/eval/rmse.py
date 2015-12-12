from eval import Eval
import numpy as np
import math

class RMSE(Eval):
  def __init__(self):
    Eval.__init__(self)
    self._previous_s = 0
    self._previous_n = 0
    self._alpha = 0.995    

  def stream_evaluate(self, truth, pred):
    ei = self.evaluate(truth, pred)
    self._previous_s = ei + self._alpha * self._previous_s
    self._previous_n = 1 + self._alpha * self._previous_n
    return float(self._previous_s) / self._previous_n

  def evaluate(self, truth, pred):
    size = truth.shape[0]
    wmse = 0.0
    for i, t in enumerate(truth):
      wmse += pow((t - pred[i]), 2)
    return math.sqrt(wmse / size)

  def best(self, tuples, idx):
    return min(tuples, key=lambda v: v[idx])

  def __str__(self):
    return 'rmse'