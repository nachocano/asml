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


class Output:
  def __init__(self, registry):
    self._registry = registry
    self._unregistered = None

  def get_unregistered(self):
    return self._unregistered

  def do_emit(self, address, examples):
    try:
      client = StreamClient(address)
      client.emit(examples)
    except Exception, ex:
      print 'exc, notify that the learner at %s is not active anymore' % address
      self._registry.unreg(ComponentType.LEARNER, address)
      self._unregistered = address

class FeatureGeneratorHandler:
  def __init__(self, registry, parser, dao, historical_batches, stream_clients_addresses):
    self._registry = registry
    self._parser = parser
    self._dao = dao
    self._stream_clients_addresses = stream_clients_addresses
    self._historical_batches = historical_batches
    self._batches = 0
    self._lock = threading.Lock()
    print 'initial stream clients: %s' % self._stream_clients_addresses

  def notify(self, addresses):
    with self._lock:
      self._stream_clients_addresses = []
      for address in addresses:
        self._stream_clients_addresses.append(address)
      print 'updated clients: %s' % self._stream_clients_addresses

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

    # TODO refactor, ugly stuff ##########################
    with self._lock:
      outputs = [Output(self._registry) for x in self._stream_clients_addresses]
      threads = []
      for i, address in enumerate(self._stream_clients_addresses):
        thread = threading.Thread(target=outputs[i].do_emit, args=(address, examples))
        threads.append(thread)
      # start threads
      for t in threads:
        t.start()
      # wait for thread completion
      for t in threads:
        t.join()
      # merging results
      unregistered_clients = []
      for out in outputs:
        candidate_unreg = out.get_unregistered()
        if candidate_unreg:
          unregistered_clients.append(candidate_unreg)
      print 'unreg clients %s' % unregistered_clients
      if len(unregistered_clients) > 0:
        self._stream_clients_addresses = Utils.diff(self._stream_clients_addresses, unregistered_clients)
        print 'updated clients: %s' % self._stream_clients_addresses

class FeatureGenerator:
  def __init__(self, dao, module_properties):
    self._dao = dao
    self._parser = ParserFactory.new_parser(module_properties)
    self._historical_batches = module_properties['historical_batches']
    self._registry = RegistryClient(module_properties['registry'])
    self._server_port = module_properties['server_port']
    hostname = socket.gethostname()
    address = Utils.get_address(hostname, self._server_port)
    self._stream_clients_addresses = self._registry.reg(ComponentType.FEATGEN, address)
    self._processor = StreamService.Processor(FeatureGeneratorHandler(self._registry, self._parser, 
                                              self._dao, self._historical_batches, self._stream_clients_addresses))
    self._stream_server = Server(self._processor, self._server_port, module_properties['multi_threading'])

  def run(self):
    self._stream_server.start()

