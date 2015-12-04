from auc import AUC
from accuracy import Accuracy

class EvaluatorFactory:

  @classmethod
  def new_evaluator(cls, evaluator):
    if evaluator == 'auc':
      return AUC()
    elif evaluator == 'accuracy':
      return accuracy()
    else:
      raise ValueException('invalid evaluator %s' % evaluator)