from asml.autogen.asml import StreamService

from asml.network.client import StreamClient
from asml.network.server import StreamServer
from handler import FeatureGeneratorHandler

class FeatureGenerator:
  def __init__(self, module_properties):
    self._stream_client = StreamClient(module_properties)
    self._processor = StreamService.Processor(FeatureGeneratorHandler(self._stream_client))
    self._stream_server = StreamServer(module_properties, self._processor)
