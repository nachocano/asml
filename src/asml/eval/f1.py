from sklearn.metrics import f1_score
from eval import Eval
import numpy as np

class F1(Eval):
  def __init__(self):
    Eval.__init__(self)
    self._preds = np.array([])
    self._truth = np.array([])

  def stream_evaluate(self, truth, preds):
    self._truth = np.hstack((self._truth, truth))
    self._preds = np.hstack((self._preds, preds))
    return f1_score(self._truth, self._preds)

  def evaluate(self, truth, preds):
    return f1_score(truth, preds)

  def best(self, tuples, idx):
    return max(tuples, key=lambda v: v[idx])

  def __str__(self):
    return 'f1'