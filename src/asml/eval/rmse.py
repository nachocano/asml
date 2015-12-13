from eval import Eval
import numpy as np
import math

class RMSE(Eval):
  def __init__(self, alpha=1):
    Eval.__init__(self, alpha)

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