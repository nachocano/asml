import time
import threading
import logging
from asml.autogen.services import StreamService
from asml.network.server import Server
from asml.eval.factory import EvaluatorFactory
from collections import defaultdict
import logging

class DeployerHandler:
  def __init__(self, evaluator, no_clients):
    self._evaluator = evaluator
    self._results = defaultdict(list)
    self._predictions = defaultdict(list)
    self._lock = threading.Lock()
    # TODO create register service and set this up
    self._no_clients = no_clients
    
  def emit(self, data):
    try:
      id, metric, timestamp = data[0].split(' ')
      metric = float(metric)
      with self._lock:
        rl = self._results[timestamp]
        rl.append((id, timestamp, metric))
        self._predictions[(id, timestamp)] = data[1:]
        if len(rl) == self._no_clients:
          id_, timestamp_, metric_ = self._evaluator.best(rl, 2)
          print 'best model %s at %s with %s' % (id_, timestamp_, metric_)
          logging.debug('%s:%s' % (timestamp_, metric_))
          self._predict(self._predictions[(id_, timestamp_)])

    except Exception, ex:
      print 'ex %s' % ex.message

  def _predict(self, predictions):
    for prediction in predictions:
      logging.debug(prediction)

class Deployer:
  def __init__(self, module_properties):
    self._evaluator = EvaluatorFactory.new_evaluator(module_properties['eval'])
    self._no_clients = module_properties['no_clients']
    self._processor = StreamService.Processor(DeployerHandler(self._evaluator, self._no_clients))
    self._stream_server = Server(self._processor, module_properties['server_port'], module_properties['multi_threading'])

  def run(self):
    self._stream_server.start()