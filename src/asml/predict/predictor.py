from asml.autogen.services import NotificationService
from asml.autogen.services import StreamService
from asml.network.server import Server
from threading import Thread

class PredictorStreamHandler:
  #def __init__(self):
  #   pass

  def emit(self, data):
    print "streaming"

class PredictorNotificationHandler:
  #def __init__(self):
  #   pass

  def best_model(self, id, timestamp):
    print "BEST MODELLLLL %s, %s" % (id, timestamp)


class Predictor:
  def __init__(self, module_properties, dao):
    self._warmup_examples = module_properties['warmup_examples']
    self._dao = dao
    self._notif_processor = NotificationService.Processor(PredictorNotificationHandler())
    self._stream_processor = StreamService.Processor(PredictorStreamHandler())
    self._notif_server = Server(self._notif_processor, module_properties['notif_server_port'], module_properties['notif_multi_threading'])
    self._stream_server = Server(self._stream_processor, module_properties['stream_server_port'], module_properties['stream_multi_threading'])

  def _init_stream(self):
    self._stream_server.start()

  def run(self):
    thread = Thread(target = self._init_stream)
    thread.daemon = True
    thread.start()
    self._notif_server.start()
