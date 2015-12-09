import logging
import gzip
import itertools
import numpy as np
from asml.network.stream import StreamClient
from asml.parser.factory import ParserFactory

class FileStream:
  def __init__(self, module_properties):
    self._path = module_properties['filename']
    self._batch_size = module_properties['batch_size']
    self._parser = ParserFactory.new_parser(module_properties)
    self._stream_client = StreamClient(module_properties)
    self._iter = self._stream_data()

  def _stream_data(self):
    for line in self._parser.parse_stream(gzip.open(self._path, 'rb')):
      yield line

  def _get_minibatch(self):
    data = list(itertools.islice(self._iter, self._batch_size))
    if not len(data):
      return []
    return list(data)

  def run(self):
    self._stream_client.open()
    data = self._get_minibatch()
    while len(data):
      self._stream_client.emit(data)
      data = self._get_minibatch()
    logging.info('no more data...')