from sklearn.metrics import mean_squared_error
from eval import Eval

class RMSE(Eval):
  def __init__(self):
    Eval.__init__(self)

  def eval(self):
    return mean_squared_error(self._truth, self._preds)

  def __str__(self):
    return 'rmse'