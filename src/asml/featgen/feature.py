from asml.autogen.services import StreamService
from asml.network.stream import StreamClient
from asml.network.server import Server
from asml.parser.factory import ParserFactory

class FeatureGeneratorHandler:
  def __init__(self, client, parser):
    self._stream_client = client
    self._parser = parser

  def emit(self, data):
    try:
      features = self._parser.parse_raw(data)
      # TODO save them into the db...
      self._stream_client.emit(features)
    except Exception, ex:
      print 'ex %s' % ex.message

class FeatureGenerator:
  def __init__(self, module_properties):
    self._parser = ParserFactory.new_parser(module_properties)
    self._stream_client = StreamClient(module_properties)
    self._processor = StreamService.Processor(FeatureGeneratorHandler(self._stream_client, self._parser))
    self._stream_server = Server(self._processor, module_properties['server_port'], module_properties['multi_threading'])

  def run(self):
    self._stream_client.open()
    self._stream_server.start()
