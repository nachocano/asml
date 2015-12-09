import abc

class Eval:
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def evaluate(self, truth, pred):
    return

  @abc.abstractmethod
  def stream_evaluate(self, truth, pred):
    return

  @abc.abstractmethod
  def best(self, tuples, idx):
    return