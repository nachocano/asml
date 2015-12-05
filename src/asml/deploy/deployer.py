from asml.util.utils import Utils
from asml.autogen.asml import StreamService
from asml.network.server import StreamServer
from asml.eval.factory import EvaluatorFactory
from collections import defaultdict

import threading

class DeployerHandler:
  def __init__(self, evaluator):
    self._evaluator = evaluator
    self._bests = defaultdict(float)
    self._lock = threading.Lock()
    
  def emit(self, data):
    id, metric, timestamp = data[0].split(' ')
    timestamp = long(timestamp)
    metric = float(metric)
    with self._lock:
      # check if we have a better one, and notify the predictor
      if self._evaluator.is_better(metric, self._bests[timestamp]):
        self._bests[timestamp] = metric
        print 'best at %s is %s with %s' % (timestamp, id, metric)

class Deployer:
  def __init__(self, module_properties):
    self._evaluator = EvaluatorFactory.new_evaluator(module_properties['eval'])
    self._processor = StreamService.Processor(DeployerHandler(self._evaluator))
    self._stream_server = StreamServer(module_properties, self._processor)

  def run(self):
    self._stream_server.start()