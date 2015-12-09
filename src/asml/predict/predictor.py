from asml.autogen.services import NotificationService
from asml.autogen.services import StreamService
from asml.network.server import Server
from asml.parser.factory import ParserFactory
from asml.eval.factory import EvaluatorFactory
from threading import Thread
from threading import Lock
import Queue
import logging

class PredictorStreamHandler:
  def __init__(self, parser, dao, evaluator, warmup_examples):
    self._parser = parser
    self._dao = dao
    self._evaluator = evaluator
    self._warmup_examples = warmup_examples
    self._best = None
    self._lock = Lock()
    self._current_timestamp = -1
    self._queue = Queue.Queue(5)

  def emit(self, data):
    try:
      X, y, timestamp = self._parser.parse_feature(data)
      if timestamp < self._warmup_examples:
        print 'warm up phase...'
        with self._lock:
          self._current_timestamp = timestamp
      else:
        predicted = False
        with self._lock:
          self._current_timestamp = timestamp
          if self._best:
            predicted = True
            predictions = self._best[0].predict(X)
            print 'predicting with model %s at %s' % (self._best[1], self._best[2])
        if predicted:
          metric = self._evaluator.evaluate(y, predictions)
          logging.debug('%s:%s', timestamp, metric)
        else:
          print 'could not predict, no model available'
    except Exception, ex:
      print 'ex %s' % ex.message
        
  def on_new_model(self, id, timestamp):
    print "new best model received: %s at %s" % (id, timestamp)
    try:
      new_clf = self._dao.get_model(id, timestamp)
      with self._lock:
        print 'queue size %d' % self._queue.qsize()
        print 'current timestamp %s' % self._current_timestamp
        if self._current_timestamp >= timestamp:
          print 'pushing model %s at %s to production' % (id, timestamp)
          self._best = (new_clf, id, timestamp)
        else:
          if not self._queue.empty():
            id_, timestamp_, old_clf_ = self._queue.get()
            if self._current_timestamp > timestamp_:
              print 'pushing model (from queue) %s at %s to production' % (id_, timestamp_)
              self._best = (old_clf_, id_, timestamp_)
          self._queue.put((id, timestamp, new_clf))
    except Exception, ex:
      print 'ex %s' % ex.message

class PredictorNotificationHandler:
  def __init__(self, stream_handler):
    self._stream_handler = stream_handler

  def best_model(self, id, timestamp):
    self._stream_handler.on_new_model(id, long(timestamp))

class Predictor:
  def __init__(self, module_properties, dao):
    self._dao = dao
    self._warmup_examples = module_properties['warmup_examples']
    self._parser = ParserFactory.new_parser(module_properties)
    self._evaluator = EvaluatorFactory.new_evaluator(module_properties['eval'])
    self._stream_handler = PredictorStreamHandler(self._parser, self._dao, self._evaluator, self._warmup_examples)
    self._notification_handler = PredictorNotificationHandler(self._stream_handler)
    self._notif_processor = NotificationService.Processor(self._notification_handler)
    self._stream_processor = StreamService.Processor(self._stream_handler)
    self._notif_server = Server(self._notif_processor, module_properties['notif_server_port'], module_properties['notif_multi_threading'])
    self._stream_server = Server(self._stream_processor, module_properties['stream_server_port'], module_properties['stream_multi_threading'])

  def _init_stream(self):
    self._stream_server.start()

  def run(self):
    thread = Thread(target = self._init_stream)
    thread.daemon = True
    thread.start()
    self._notif_server.start()
