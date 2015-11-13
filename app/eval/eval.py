import abc
import numpy as np

class Eval:
  __metaclass__ = abc.ABCMeta

  def __init__(self):
    self._child = None

  def set_child(self, value):
    self._child = value
    self._preds = np.array([])
    self._truth = np.array([])

  def next(self):
    # TODO improve this
    for i, truth, pred in self._child.next():
      self._truth = np.hstack((self._truth, truth))
      self._preds = np.hstack((self._preds, pred))
      metric = self.eval()
      print 'batch %s -> %s %s' % (i, str(self), metric)

  @abc.abstractmethod
  def eval(self):
    return
