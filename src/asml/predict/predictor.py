from asml.autogen.services import NotificationService
from asml.autogen.services import StreamService
from asml.network.server import Server
from asml.parser.factory import ParserFactory
from threading import Thread
from threading import Lock

class PredictorStreamHandler:
  def __init__(self, parser, dao, warmup_examples):
    self._parser = parser
    self._dao = dao
    self._warmup_examples = warmup_examples
    self._clf = None
    self._lock = Lock()

  def emit(self, data):
    X, y, timestamp = self._parser.parse_feature(data)
    if timestamp < self._warmup_examples:
      print 'warmed up phase'
    else:
      pass

  def on_new_model(self, id, timestamp):
    new_clf = self._dao.get_model(id, timestamp)
    print "on_new_model succeed"

class PredictorNotificationHandler:
  def __init__(self, stream_handler):
    self._stream_handler = stream_handler

  def best_model(self, id, timestamp):
    print "new best model received: %s at %s" % (id, timestamp)
    self._stream_handler.on_new_model(id, timestamp)

class Predictor:
  def __init__(self, module_properties, dao):
    self._warmup_examples = module_properties['warmup_examples']
    self._parser = ParserFactory.new_parser(module_properties['parser'])
    self._dao = dao
    self._stream_handler = PredictorStreamHandler(self._parser, self._dao, self._warmup_examples)
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
