import abc

class Eval:
  __metaclass__ = abc.ABCMeta

  def __init__(self, alpha=1):
    self._alpha = alpha
    self._previous_s = 0
    self._previous_n = 0

  @abc.abstractmethod
  def evaluate(self, truth, pred):
    return

  def stream_evaluate(self, truth, pred):
    ei = self.evaluate(truth, pred)
    self._previous_s = ei + self._alpha * self._previous_s
    self._previous_n = 1 + self._alpha * self._previous_n
    return float(self._previous_s) / self._previous_n

  @abc.abstractmethod
  def best(self, tuples, idx):
    return