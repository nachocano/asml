from sklearn.metrics import roc_curve, auc
import numpy as np
from eval import Eval

class AUC(Eval):
  def __init__(self):
    Eval.__init__(self)
    self._preds = np.array([])
    self._truth = np.array([])

  def stream_eval(self, truth, pred):
    self._truth = np.hstack((self._truth, truth))
    self._preds = np.hstack((self._preds, pred))
    fpr, tpr, _ = roc_curve(self._truth, self._preds)
    return auc(fpr, tpr)

  def __str__(self):
    return 'auc'