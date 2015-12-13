from eval import Eval
import numpy as np
from sklearn.metrics import zero_one_loss


class ZeroOne(Eval):
  def __init__(self, alpha=1):
    Eval.__init__(self, alpha)

  def _as_int(self,x):
    return round(x)

  def evaluate(self, truth, pred):
    return zero_one_loss(truth, map(self._as_int, pred))

  def best(self, tuples, idx):
    return min(tuples, key=lambda v: v[idx])

  def __str__(self):
    return '0/1'