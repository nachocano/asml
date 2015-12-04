from asml.autogen.asml import StreamService
from asml.network.client import StreamClient
from asml.network.server import StreamServer

class FeatureGeneratorHandler:
  def __init__(self, client):
    self._stream_client = client

  def emit(self, data):
    print(data)
    self._stream_client.emit(data)


class FeatureGenerator:
  def __init__(self, module_properties):
    self._stream_client = StreamClient(module_properties)
    self._processor = StreamService.Processor(FeatureGeneratorHandler(self._stream_client))
    self._stream_server = StreamServer(module_properties, self._processor)

  def run(self):
    self._stream_server.start()
