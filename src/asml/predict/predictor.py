from asml.autogen.services import NotificationService
from asml.network.server import Server

class PredictorHandler:
  # def __init__(self):
  #   pass

  def emit(self, data):
    print data

  def best_model(id, timestamp):
    print "predictor %s, %s" % (id, timestamp)


class Predictor:
  def __init__(self, module_properties, dao):
    self._warmup_examples = module_properties['warmup_examples']
    self._dao = dao
    self._handler = PredictorHandler()
    self._processor = NotificationService.Processor(self._handler)
    self._server = Server(module_properties, self._processor)

  def run(self):
    self._server.start()