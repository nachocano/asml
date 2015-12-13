from eval import Eval
import numpy as np
from sklearn.metrics import log_loss

class LogLoss(Eval):
  def __init__(self, alpha=1):
    Eval.__init__(self, alpha)

  def evaluate(self, truth, pred):
    return log_loss(truth, pred)

  def best(self, tuples, idx):
    return min(tuples, key=lambda v: v[idx])

  def __str__(self):
    return 'logloss'