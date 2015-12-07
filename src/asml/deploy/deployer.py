from asml.autogen.services import StreamService
from asml.network.server import Server
from asml.network.notification import NotificationClient
from asml.eval.factory import EvaluatorFactory
from collections import defaultdict

import threading

class DeployerHandler:
  def __init__(self, evaluator, notification_client):
    self._evaluator = evaluator
    self._notification_client = notification_client
    self._bests = defaultdict(float)
    self._lock = threading.Lock()
    
  def emit(self, data):
    id, metric, timestamp = data[0].split(' ')
    metric = float(metric)
    with self._lock:
      # check if we have a better one, and notify the predictor
      if self._evaluator.is_better(metric, self._bests[timestamp]):
        self._bests[timestamp] = metric
        print 'best at %s is %s with %s' % (timestamp, id, metric)
        #self._notif_client.best_model(id, timestamp)

class Deployer:
  def __init__(self, module_properties):
    self._evaluator = EvaluatorFactory.new_evaluator(module_properties['eval'])
    self._notification_client = NotificationClient(module_properties)
    self._processor = StreamService.Processor(DeployerHandler(self._evaluator, self._notification_client))
    self._stream_server = Server(module_properties, self._processor)

  def run(self):
    self._notification_client.open()
    self._stream_server.start()