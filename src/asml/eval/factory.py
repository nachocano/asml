from auc import AUC
from accuracy import Accuracy
from f1 import F1

class EvaluatorFactory:

  @classmethod
  def new_evaluator(cls, evaluator):
    if evaluator == 'auc':
      return AUC()
    elif evaluator == 'accuracy':
      return Accuracy()
    elif evaluator == 'f1':
      return F1()
    else:
      raise ValueException('invalid evaluator %s' % evaluator)