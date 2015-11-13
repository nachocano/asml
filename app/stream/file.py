import itertools
import numpy as np
from app.parser.svm import SVMLightParser

class FileStream:
  def __init__(self, config):
    self._path = config['stream']
    self._batch_size = config['batch_size']
    if config['parser']:
      self._parser = SVMLightParser()
    else:
      raise Exception("only SVMLight format supported")
    self._iter = self._stream_data()

  def _stream_data(self):
    for instance in self._parser.parse(open(self._path, 'r')):
      yield instance

  def _get_minibatch(self):
    """
    Extract a minibatch of examples, return a tuple X, y.
    """
    data = list(itertools.islice(self._iter, self._batch_size))
    if not len(data):
      return np.asarray([], dtype=np.float32), np.asarray([], dtype=int)
    X, y = zip(*data)
    return np.asarray(X, dtype=np.float32), np.asarray(y, dtype=int)

  def iter_minibatches(self):
    """Generator of minibatches."""
    X, y = self._get_minibatch()
    while len(X):
      yield X, y
      X, y = self._get_minibatch()




