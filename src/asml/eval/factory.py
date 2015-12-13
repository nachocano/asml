from auc import AUC
from accuracy import Accuracy
from rmse import RMSE
from logloss import LogLoss

class EvaluatorFactory:

  @classmethod
  def new_evaluator(cls, evaluator):
    if evaluator == 'auc':
      return AUC()
    elif evaluator == 'accuracy':
      return Accuracy()
    elif evaluator == 'rmse':
      return RMSE()
    elif evaluator == 'log_loss':
      return LogLoss()
    else:
      raise ValueError('invalid evaluator %s' % evaluator)