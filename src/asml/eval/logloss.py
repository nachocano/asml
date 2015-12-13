from eval import Eval
import numpy as np
from sklearn.metrics import log_loss

class LogLoss(Eval):
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
    return log_loss(truth, pred)

  def best(self, tuples, idx):
    return min(tuples, key=lambda v: v[idx])

  def __str__(self):
    return 'logloss'