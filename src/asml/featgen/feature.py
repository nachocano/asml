import socket
import threading
from asml.autogen.services import StreamService
from asml.autogen.services.ttypes import ComponentType
from asml.network.stream import StreamClient
from asml.network.server import Server
from asml.parser.factory import ParserFactory
from asml.network.registry import RegistryClient
from asml.util.utils import Utils


class FeatureGeneratorHandler:
  def __init__(self, parser, dao, historical_batches, stream_client_addresses):
    self._parser = parser
    self._dao = dao
    self._stream_clients = []
    for stream_client_address in stream_client_addresses:
      self._stream_clients.append(StreamClient(stream_client_address))
    self._historical_batches = historical_batches
    self._batches = 0
    self._lock = threading.Lock()

  def notify(self, addresses):
    with self._lock:
      self._stream_clients = []
      for address in addresses:
        self._stream_clients.append(StreamClient(address))

  def emit(self, data):
    try:
      examples = self._parser.parse_raw(data)
      self._dao.save_examples(examples[1:])
      self._batches += 1
      # TODO put this in another thread
      if self._batches > self._historical_batches:
        batch_size = len(data)
        # get last timestamp of batch
        last_timestamp = long(examples[-1].split(' ')[0])
        # max timestamp to delete
        max_timestamp = last_timestamp - self._historical_batches * batch_size
        self._dao.delete_examples(max_timestamp)
        self._batches = 0
    except Exception, ex:
      print 'ex %s' % ex.message
      return

    print 'here'
    with self._lock:
      print 'after lock'
      threads = []
      for stream_client in self._stream_clients:
        thread = threading.Thread(target=self._do_emit, args=(stream_client, examples))
        threads.append(thread)
      # start threads
      for t in threads:
        t.start()
      # wait for thread completion
      for t in threads:
        t.join()

  def _do_emit(self, stream_client, examples):
    try:
      stream_client.emit(examples)
    except Exception, ex:
      print 'TODO exc'

class FeatureGenerator:
  def __init__(self, dao, module_properties):
    self._dao = dao
    self._parser = ParserFactory.new_parser(module_properties)
    self._historical_batches = module_properties['historical_batches']
    self._registry = RegistryClient(module_properties['registry'])
    self._server_port = module_properties['server_port']
    hostname = socket.gethostname()
    address = Utils.get_address(hostname, self._server_port)
    self._stream_client_addresses = self._registry.reg(ComponentType.FEATGEN, address)
    self._processor = StreamService.Processor(FeatureGeneratorHandler(self._parser, 
                                              self._dao, self._historical_batches, self._stream_client_addresses))
    self._stream_server = Server(self._processor, self._server_port, module_properties['multi_threading'])

  def run(self):
    self._stream_server.start()

