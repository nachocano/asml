import itertools
import numpy as np
from asml.network.client import StreamClient

class FileStream:
  def __init__(self, module_properties):
    self._path = module_properties['filename']
    self._batch_size = module_properties['batch_size']
    self._stream_client = StreamClient(module_properties)
    self._iter = self._stream_data()

  def _stream_data(self):
    for line in open(self._path, 'r'):
      yield line

  def _get_minibatch(self):
    data = list(itertools.islice(self._iter, self._batch_size))
    if not len(data):
      return []
    return list(data)

  def run(self):
    data = self._get_minibatch()
    while len(data):
      self._stream_client.emit(data)
      data = self._get_minibatch()
    print 'no more data...'