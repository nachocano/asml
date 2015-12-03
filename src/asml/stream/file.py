import itertools
import numpy as np
from asml.parser.svm import SVMLightParser

class FileStream:
  def __init__(self, app_properties):
    self._path = app_properties['stream']
    self._batch_size = app_properties['batch_size']
    if app_properties['parser']:
      self._parser = SVMLightParser()
    else:
      raise Exception("only svm format supported")
    self._iter = self._stream_data()

  def _stream_data(self):
    for instance in self._parser.parse(open(self._path, 'r')):
      yield instance

  def _get_minibatch(self):
    data = list(itertools.islice(self._iter, self._batch_size))
    if not len(data):
      return np.asarray([], dtype=int), np.asarray([], dtype=int)
    X, y = zip(*data)
    return np.asarray(X, dtype=np.float32), np.asarray(y, dtype=int)

  def next(self):
    X, y = self._get_minibatch()
    while len(X):
      yield X, y
      X, y = self._get_minibatch()




