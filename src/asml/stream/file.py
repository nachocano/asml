import gzip
import itertools
from asml.network.registry import RegistryClient
from asml.network.stream import StreamClient
from asml.autogen.services.ttypes import ComponentType
from asml.parser.factory import ParserFactory

class FileStream:
  def __init__(self, module_properties):
    self._path = module_properties['filename']
    self._batch_size = module_properties['batch_size']
    self._parser = ParserFactory.new_parser(module_properties)
    self._registry = RegistryClient(module_properties['registry'])
    self._iter = self._stream_data()
    self._featgen_client = None

  def _stream_data(self):
    for line in self._parser.parse_stream(gzip.open(self._path, 'rb')):
      yield line

  def _get_minibatch(self):
    data = list(itertools.islice(self._iter, self._batch_size))
    if not len(data):
      return []
    return list(data)

  def run(self):
    stream_client_address = self._registry.reg(ComponentType.DATASTREAM, 'DUMMY')[0]
    # Just considering one stream_client for now (FeatureGenerator)
    self._featgen_client = StreamClient(stream_client_address)
    data = self._get_minibatch()
    while len(data):
        self._featgen_client.emit(data)
        data = self._get_minibatch()
    print 'no more data...'