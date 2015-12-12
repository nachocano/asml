from eval import Eval
import numpy as np
import math

class RMSE(Eval):
  def __init__(self):
    Eval.__init__(self)
    self._preds = np.array([])
    self._truth = np.array([])

  def stream_evaluate(self, truth, pred):
    self._truth = np.hstack((self._truth, truth))
    self._preds = np.hstack((self._preds, pred))
    return self.evaluate(self._truth, self._preds)

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