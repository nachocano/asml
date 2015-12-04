import numpy as np

from asml.autogen.asml import StreamService
from asml.network.client import StreamClient
from asml.network.server import StreamServer
from asml.util.utils import Utils
from asml.model.serializer import Serializer
from asml.parser.factory import ParserFactory

class LearnerHandler:
  def __init__(self, client, parser, clf, classes):
    self._stream_client = client
    self._parser = parser
    self._clf = clf
    self._classes = classes

  def emit(self, data):
    X, y, timestamp = self._parser.parse_feature(data)
    #self._stream_client.emit(data)

class Learner:
  def __init__(self, module_properties, dao, clf):
    self._name = module_properties['name']
    self._warmup_batches = module_properties['warmup_batches']
    self._parser = ParserFactory.new_parser(module_properties['parser'])
    self._dao = dao
    self._clf = clf
    self._classes = np.array(map(int, module_properties['classes'].split(',')))
    self._stream_client = StreamClient(module_properties)
    self._handler = LearnerHandler(self._stream_client, self._parser, self._clf, self._classes)
    self._processor = StreamService.Processor(self._handler)
    self._stream_server = StreamServer(module_properties, self._processor)

  def run(self):
    self._stream_server.start()
    # for i, (X, y) in enumerate(self._child.next()):
    #   # just train
    #   if Utils.warmup(self._warmup_batches, i):
    #     # train
    #     self._clf.partial_fit(X, y, classes=self._classes)
    #     yield i, self._clf
    #   else:
    #     # predict
    #     predictions = self._clf.predict(X)
    #     # then train
    #     self._clf.partial_fit(X, y, classes=self._classes)
    #     # return ground truth, predictions and model
    #     yield i, self._clf, y, predictions


  def _save_model(self, timestamp, clf):
    self._dao.save_model(timestamp, self._name, Serializer.serialize(clf), self._current_eval)
