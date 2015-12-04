from asml.util.utils import Utils
from asml.autogen.asml import StreamService
from asml.network.server import StreamServer
from collections import defaultdict

class DeployerHandler:
  def __init__(self):
    self._count = 0

  def emit(self, data):
    print data

class Deployer:
  def __init__(self, module_properties):
    self._processor = StreamService.Processor(DeployerHandler())
    self._stream_server = StreamServer(module_properties, self._processor)


  def run(self):
    self._stream_server.start()