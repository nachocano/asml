from asml.autogen.asml import StreamService
from asml.network.client import StreamClient
from asml.network.server import StreamServer
from asml.parser.factory import ParserFactory

class FeatureGeneratorHandler:
  def __init__(self, client, parser):
    self._stream_client = client
    self._parser = parser

  def emit(self, data):
    features = self._parser.parse_raw(data)
    # save them into the db...
    self._stream_client.emit(features)

class FeatureGenerator:
  def __init__(self, module_properties):
    self._parser = ParserFactory.new_parser(module_properties['parser'])
    self._stream_client = StreamClient(module_properties)
    self._processor = StreamService.Processor(FeatureGeneratorHandler(self._stream_client, self._parser))
    self._stream_server = StreamServer(module_properties, self._processor)

  def run(self):
    self._stream_server.start()
