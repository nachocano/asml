import logging
import numpy as np

from asml.autogen.services import StreamService
from asml.network.stream import StreamClient
from asml.network.server import Server
from asml.parser.factory import ParserFactory
from asml.eval.factory import EvaluatorFactory

class LearnerHandler:
  def __init__(self, client, parser, evaluator, dao, clf, classes, warmup_examples, id):
    self._stream_client = client
    self._parser = parser
    self._evaluator = evaluator
    self._dao = dao
    self._current_best = self._evaluator.default()
    self._clf = clf
    self._classes = classes
    self._warmup_examples = warmup_examples
    self._id = id

  def emit(self, data):
    X, y, timestamp = self._parser.parse_feature(data)
    if timestamp < self._warmup_examples:
      # train
      self._clf.partial_fit(X, y, classes=self._classes)
      # predict (so that we can have a warmed up model)
      # the predictor should not predict in the warming phase
      predictions = self._clf.predict(X)
    else:
      # predict (regular case)
      predictions = self._clf.predict(X)
      # then train
      self._clf.partial_fit(X, y, classes=self._classes)

    # evaluate
    new_metric = self._evaluator.evaluate(y, predictions)
    # if warmup, just save the model with default metric, and send it to deployer
    # so that he can take care of it...
    if timestamp < self._warmup_examples:
      self._dao.save_model(timestamp, self._id, self._clf, self._evaluator.default())
      self._stream_client.emit(['%s %s %s' % (self._id, new_metric, timestamp)])
    else:
      logging.debug('%s:%s', timestamp, new_metric)
      # check if we improve
      if self._evaluator.is_better_or_equal(new_metric, self._current_best):
        self._current_best = new_metric
        # persist the current best
        self._dao.save_model(timestamp, self._id, self._clf, new_metric)
        # send it to the deployer, so that he can decide if this is the overall best
        self._stream_client.emit(['%s %s %s' % (self._id, self._current_best, timestamp)])

class Learner:
  def __init__(self, module_properties, dao, clf):
    self._id = module_properties['id']
    self._warmup_examples = module_properties['warmup_examples']
    self._parser = ParserFactory.new_parser(module_properties['parser'])
    self._evaluator = EvaluatorFactory.new_evaluator(module_properties['eval'])
    self._dao = dao
    self._clf = clf
    self._classes = np.array(map(int, module_properties['classes'].split(',')))
    self._stream_client = StreamClient(module_properties)
    self._handler = LearnerHandler(self._stream_client, self._parser, self._evaluator, self._dao, self._clf, self._classes, self._warmup_examples, self._id)
    self._processor = StreamService.Processor(self._handler)
    self._stream_server = Server(self._processor, module_properties['server_port'], module_properties['multi_threading'])

  def run(self):
    self._stream_client.open()
    self._stream_server.start()