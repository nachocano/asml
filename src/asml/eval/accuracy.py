from eval import Eval
import numpy as np

class Accuracy(Eval):
  def __init__(self, alpha=1):
    Eval.__init__(self, alpha)

  def evaluate(self, truth, pred):
    return float(np.sum(truth == pred)) / truth.shape[0]

  def best(self, tuples, idx):
    return max(tuples, key=lambda v: v[idx])    

  def __str__(self):
    return 'accuracy'