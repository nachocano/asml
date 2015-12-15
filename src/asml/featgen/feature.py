import socket
import threading
import copy
from asml.autogen.services import StreamService
from asml.autogen.services.ttypes import ComponentType
from asml.network.stream import StreamClient
from asml.network.server import Server
from asml.parser.factory import ParserFactory
from asml.network.registry import RegistryClient
from asml.util.utils import Utils



class FeatureGeneratorHandler:
  def __init__(self, registry, parser, dao, historical_batches, stream_client_addresses):
    self._registry = registry
    self._parser = parser
    self._dao = dao
    self._stream_clients_addresses = stream_client_addresses
    self._historical_batches = historical_batches
    self._batches = 0
    self._lock = threading.Lock()

  def notify(self, addresses):
    with self._lock:
      self._stream_clients = []
      for address in addresses:
        self._stream_clients_addresses.append(address)

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

    with self._lock:
      copy_addresses = copy.deepcopy(self._stream_clients_addresses)

    # TODO threadpool with futures
    threads = []
    for address in copy_addresses:
      thread = threading.Thread(target=self._do_emit, args=(address, examples))
      threads.append(thread)
    # start threads
    for t in threads:
      t.start()
    # wait for thread completion
    for t in threads:
      t.join()

  def _do_emit(self, address, examples):
    try:
      client = StreamClient(address)
      client.emit(examples)
    except Exception, ex:
      print 'exc, notify that the learner is not active anymore'
      self._registry.unreg(ComponentType.LEARNER, address)

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
    self._processor = StreamService.Processor(FeatureGeneratorHandler(self._registry, self._parser, 
                                              self._dao, self._historical_batches, self._stream_client_addresses))
    self._stream_server = Server(self._processor, self._server_port, module_properties['multi_threading'])

  def run(self):
    self._stream_server.start()

