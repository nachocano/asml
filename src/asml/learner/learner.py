import logging
import numpy as np

from asml.autogen.services import StreamService
from asml.network.stream import StreamClient
from asml.network.server import Server
from asml.parser.factory import ParserFactory
from asml.eval.factory import EvaluatorFactory

class LearnerHandler:
  def __init__(self, client, parser, evaluator, dao, clf, test, classes, warmup_examples, id, checkpoint):
    self._stream_client = client
    self._parser = parser
    self._evaluator = evaluator
    self._dao = dao
    self._test = test
    self._clf = clf
    self._classes = classes
    self._warmup_examples = warmup_examples
    self._id = id
    self._checkpoint = checkpoint
    self._batches = 0
    self._checkpointed = False

  def emit(self, data):
    try:
      X, y, timestamps = self._parser.parse_feature(data)
      self._batches += 1
      
      if timestamps[-1] < self._warmup_examples:
        # just train
        print 'warming up at %s' % timestamps[-1]
        self._clf.partial_fit(X, y, classes=self._classes)
      else:
        # predict streaming data
        streaming_predictions = self._clf.predict(X)
        # train on streaming data
        self._clf.partial_fit(X, y, classes=self._classes)
        # predict on offline data
        offline_predictions = self._clf.predict(self._test[0])
        # evaluate on the offline data
        offline_metric = self._evaluator.evaluate(self._test[1], offline_predictions)
        # debug
        logging.debug('offline:%s:%s', timestamps[-1], offline_metric)
        # build message to emit
        header = '%s %s %s' % (self._id, offline_metric, timestamps[-1])
        body = self._stack(timestamps, y, streaming_predictions)
        body.insert(0, header)
        # emit message, deployer will see who is the overall best
        self._stream_client.emit(body)
      
      # checkpointing model every x number of batches
      if self._batches >= self._checkpoint:
        print 'checkpointing model at %s' % timestamps[-1]
        if self._checkpointed:
          self._dao.update_model(self._id, self._clf)
        else:
          self._dao.save_model(self._id, self._clf)
          self._checkpointed = True
        self._batches = 0

    except Exception, ex:
      print 'ex %s' % ex.message

  def _stack(self, timestamps, y, y_hat, log=True):
    stacked = []
    for i, t in enumerate(timestamps):
      line = '%s %s %s' % (t, y[i], y_hat[i])
      stacked.append(line)
      if log:
        logging.debug(line)
    return stacked

class Learner:
  def __init__(self, module_properties, dao, clf):
    self._dao = dao
    self._clf = clf
    self._id = module_properties['id']
    self._warmup_examples = module_properties['warmup_examples']
    self._checkpoint = module_properties['checkpoint']
    self._parser = ParserFactory.new_parser(module_properties)
    self._evaluator = EvaluatorFactory.new_evaluator(module_properties['eval'])
    self._offline_test = self._parser.parse(module_properties['offline_test'])
    self._classes = np.array(map(int, module_properties['classes'].split(',')))
    self._stream_client = StreamClient(module_properties)
    self._handler = LearnerHandler(self._stream_client, self._parser, self._evaluator, self._dao, self._clf, self._offline_test, 
                              self._classes, self._warmup_examples, self._id, self._checkpoint)
    self._processor = StreamService.Processor(self._handler)
    self._stream_server = Server(self._processor, module_properties['server_port'], module_properties['multi_threading'])

  def run(self):
    self._stream_client.open()
    self._stream_server.start()