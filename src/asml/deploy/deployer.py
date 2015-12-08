from asml.autogen.services import StreamService
from asml.network.server import Server
from asml.network.notification import NotificationClient
from asml.eval.factory import EvaluatorFactory
from collections import defaultdict

import threading

class DeployerHandler:
  def __init__(self, evaluator, notification_client, warmup_examples):
    self._evaluator = evaluator
    self._notification_client = notification_client
    self._warmup_examples = warmup_examples
    self._bests = defaultdict(float)
    self._best_warmup = self._evaluator.default()
    self._lock = threading.Lock()
    
  def emit(self, data):
    try:    
      id, metric, timestamp = data[0].split(' ')
      metric = float(metric)
      with self._lock:
        if long(timestamp) < self._warmup_examples:
          if self._evaluator.is_better(metric, self._best_warmup):
            self._best_warmup = metric
            print 'best warmup at %s is %s with %s' % (timestamp, id, metric)
            self._notification_client.best_model(id, timestamp)
        else:
          # check if we have a better one, and notify the predictor
          if self._evaluator.is_better(metric, self._bests[timestamp]):
            self._bests[timestamp] = metric
            print 'best at %s is %s with %s' % (timestamp, id, metric)
            self._notification_client.best_model(id, timestamp)
    except Exception, ex:
      print 'ex %s' % ex.message            

class Deployer:
  def __init__(self, module_properties):
    self._warmup_examples = module_properties['warmup_examples']
    self._evaluator = EvaluatorFactory.new_evaluator(module_properties['eval'])
    self._notification_client = NotificationClient(module_properties)
    self._processor = StreamService.Processor(DeployerHandler(self._evaluator, self._notification_client, self._warmup_examples))
    self._stream_server = Server(self._processor, module_properties['server_port'], module_properties['multi_threading'])

  def run(self):
    self._notification_client.open()
    self._stream_server.start()