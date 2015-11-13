from sklearn.metrics import roc_curve, auc
from eval import Eval

class AUC(Eval):
  def __init__(self):
    Eval.__init__(self)

  def eval(self):
    fpr, tpr, thresholds = roc_curve(self._truth, self._preds)
    return auc(fpr, tpr)

  def __str__(self):
    return 'auc'