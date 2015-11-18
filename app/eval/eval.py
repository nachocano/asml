import abc

class Eval:
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def stream_eval(self, truth, pred):
    return

  def default(self):
    return 0.0

  def is_better(self, new, old):
    return new >= old