import numpy as np

from asml.autogen.asml import StreamService
from asml.network.client import StreamClient
from asml.network.server import StreamServer
from asml.util.utils import Utils

class LearnerHandler:
  def __init__(self, client):
    self._stream_client = client

  def emit(self, data):
    print data
    #self._stream_client.emit(data)

class Learner:
  def __init__(self, module_properties, clf):
    self._warmup_batches = module_properties['warmup_batches']
    self._clf = clf
    self._classes = np.array(map(int, module_properties['classes'].split(',')))
    self._stream_client = StreamClient(module_properties)
    self._processor = StreamService.Processor(LearnerHandler(self._stream_client))
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
