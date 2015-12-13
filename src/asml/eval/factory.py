from auc import AUC
from accuracy import Accuracy
from rmse import RMSE
from logloss import LogLoss
from zeroone import ZeroOne

class EvaluatorFactory:

  @classmethod
  def new_evaluator(cls, module_properties):
    evaluator = module_properties['eval']
    alpha = 1
    if module_properties.has_key('eval_alpha'):
      alpha = module_properties['eval_alpha']

    if evaluator == 'auc':
      return AUC(alpha)
    elif evaluator == 'accuracy':
      return Accuracy(alpha)
    elif evaluator == 'rmse':
      return RMSE(alpha)
    elif evaluator == 'log_loss':
      return LogLoss(alpha)
    elif evaluator == 'zero_one':
      return ZeroOne(alpha)
    else:
      raise ValueError('invalid evaluator %s' % evaluator)