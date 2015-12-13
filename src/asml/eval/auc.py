from sklearn.metrics import roc_curve, auc
import numpy as np
from eval import Eval

class AUC(Eval):
  def __init__(self, alpha=1):
    Eval.__init__(self, alpha)

  def evaluate(self, truth, preds):
    fpr, tpr, _ = roc_curve(truth, preds)
    return auc(fpr, tpr)

  def best(self, tuples, idx):
    return max(tuples, key=lambda v: v[idx])

  def __str__(self):
    return 'auc'