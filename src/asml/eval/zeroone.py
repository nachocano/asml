from sklearn.metrics import zero_one_loss
from eval import Eval
import numpy as np
import math

class ZeroOne(Eval):
  def __init__(self):
    Eval.__init__(self)
    # Prequential with fading factor
    self._previous_s = 0
    self._previous_n = 0
    self._alpha = 0.995

  def stream_evaluate(self, truth, preds):
    zol = zero_one_loss(truth, preds)
    current_s = zol + self._alpha * self._previous_s
    current_n = 1 + self._alpha * self._previous_n
    self._previous_s = current_s
    self._previous_n = current_n
    return float(current_s) / current_n

  def evaluate(self, truth, preds):
    return zero_one_loss(truth, preds)

  def best(self, tuples, idx):
    best_ = tuples[0]
    for t in tuples[1:]:
      qi = math.log10(float(best_[idx]) / t[idx])
      # check if less or greater 
      # according to the paper it should be less than
      # but it doesn't make sense.
      if qi > 0:
        best_ = t
    return best_

  def __str__(self):
    return '0/1'