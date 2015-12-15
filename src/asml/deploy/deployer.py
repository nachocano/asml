import threading
import logging
import socket
from asml.network.registry import RegistryClient
from asml.autogen.services import StreamService
from asml.autogen.services.ttypes import ComponentType
from asml.network.server import Server
from asml.eval.factory import EvaluatorFactory
from asml.util.utils import Utils
from collections import defaultdict

class DeployerHandler:
  def __init__(self, evaluator):
    self._evaluator = evaluator
    self._results = defaultdict(list)
    self._predictions = defaultdict(list)
    self._lock = threading.Lock()
    # TODO make notify work
    self._no_clients = 3
    
  def notify(self, addresses):
    with self._lock:
      self._no_clients = len(addresses)

  def emit(self, data):
    try:
      id, metric, timestamp = data[0].split(' ')
      metric = float(metric)
      with self._lock:
        self._results[timestamp].append((id, timestamp, metric))
        self._predictions[(id, timestamp)] = data[1:]
        if len(self._results[timestamp]) == self._no_clients:
          id_, timestamp_, metric_ = self._evaluator.best(self._results[timestamp], 2)
          print 'best model %s at %s with %s' % (id_, timestamp_, metric_)
          logging.debug('%s:%s' % (timestamp_, metric_))
          self._predict(self._predictions[(id_, timestamp_)])
          del self._results[timestamp_]
          del self._predictions[(id_, timestamp_)]

    except Exception, ex:
      print 'ex %s' % ex.message

  def _predict(self, predictions):
    for prediction in predictions:
      logging.debug(prediction)

class Deployer:
  def __init__(self, module_properties):
    self._server_port = module_properties['server_port']
    self._evaluator = EvaluatorFactory.new_evaluator(module_properties)
    self._registry = RegistryClient(module_properties['registry'])
    self._processor = StreamService.Processor(DeployerHandler(self._evaluator))
    self._stream_server = Server(self._processor, self._server_port, module_properties['multi_threading'])


  def run(self):
    hostname = socket.gethostname()
    address = Utils.get_address(hostname, self._server_port)
    self._registry.reg(ComponentType.DEPLOYER, address)
    self._stream_server.start()
