import logging
import socket
import numpy as np

from asml.autogen.services import StreamService
from asml.autogen.services.ttypes import ComponentType
from asml.network.stream import StreamClient
from asml.network.registry import RegistryClient
from asml.network.server import Server
from asml.parser.factory import ParserFactory
from asml.eval.factory import EvaluatorFactory
from asml.util.utils import Utils

class LearnerHandler:
  def __init__(self, client_address, registry, parser, evaluator, dao, clf, classes, warmup_examples, 
              id, checkpoint, prequential, checkpointed, test):
    self._stream_client = StreamClient(client_address)
    self._registry = registry
    self._parser = parser
    self._evaluator = evaluator
    self._dao = dao
    self._clf = clf
    self._classes = classes
    self._warmup_examples = warmup_examples
    self._id = id
    self._checkpoint = checkpoint
    self._is_prequential = prequential
    assert self._is_prequential == (test == None)
    if test:
      self._test = test
    self._batches = 0
    self._checkpointed = checkpointed
    self._is_first = True
    self._streaming_metric = 0


  def notify(self, addresses):
    pass

  def emit(self, data):
    try:
      X, y, timestamps = self._parser.parse_feature(data)
      self._batches += 1
      
      if timestamps[-1] < self._warmup_examples:
        # just train
        print 'warming up at %s' % timestamps[-1]
        if self._is_first:
          self._clf.partial_fit(X, y, classes=self._classes)
          self._is_first = False
        else:
          streaming_predictions = self._clf.predict_proba(X)
          self._clf.partial_fit(X, y, classes=self._classes)
          self._streaming_metric = self._evaluator.stream_evaluate(y, streaming_predictions[:,1])
      else:
        # predict streaming data
        streaming_predictions = self._clf.predict_proba(X)

        # prequential predictions
        if self._is_prequential:
            logging.debug('%s:%s', timestamps[-1], self._streaming_metric)
            self._build_and_send(self._streaming_metric, timestamps, y, streaming_predictions)
        # holdout predictions
        else:
          self._holdout(timestamps, y, streaming_predictions)

        # now update the model (we assume we receive the label "later", though it comes in the batch)
        self._clf.partial_fit(X, y, classes=self._classes)
        if self._is_prequential:
          # also update the streaming metric to use in the next batch
          self._streaming_metric = self._evaluator.stream_evaluate(y, streaming_predictions[:,1])

      
      # checkpointing model every x number of batches
      if self._batches >= self._checkpoint:
        print 'checkpointing model at %s' % timestamps[-1]
        if self._checkpointed:
          self._dao.update_model(self._id, timestamps[-1], self._clf)
        else:
          self._dao.save_model(self._id, timestamps[-1], self._clf)
          self._checkpointed = True
        self._batches = 0

    except Exception, ex:
      print 'ex %s' % ex.message

  def _build_and_send(self, metric, timestamps, y, streaming_predictions):
    header = '%s %s %s' % (self._id, metric, timestamps[-1])
    body = self._stack(timestamps, y, streaming_predictions[:,1])
    body.insert(0, header)
    # emit message, deployer will see who is the overall best
    self._stream_client.emit(body)

  def _prequential(self, timestamps, y, streaming_predictions):
    logging.debug('%s:%s', timestamps[-1], self._streaming_metric)
    self._build_and_send(previous_metric, timestamps, streaming_predictions)

  def _holdout(self, timestamps, y, streaming_predictions):
    # predict on offline data
    offline_predictions = self._clf.predict_proba(self._test[0])
    # evaluate on the offline data
    offline_metric = self._evaluator.evaluate(self._test[1], offline_predictions[:,1])
    # debug
    logging.debug('%s:%s', timestamps[-1], offline_metric)
    # build message and emit
    self._build_and_send(offline_metric, timestamps, y, streaming_predictions)

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
    self._id = module_properties['id']
    self._clf, timestamp = self._dao.get_model(self._id)
    self._checkpointed = True
    print timestamp
    if not self._clf:
      # TODO get the historical data and train...
      self._clf = clf
      self._checkpointed = False
    self._warmup_examples = module_properties['warmup_examples']
    self._checkpoint = module_properties['checkpoint']
    self._is_prequential = True if module_properties['eval_mode'] == 'prequential' else False
    self._parser = ParserFactory.new_parser(module_properties)
    self._evaluator = EvaluatorFactory.new_evaluator(module_properties)
    self._offline_test = None
    if self._is_prequential == False:
      self._offline_test = self._parser.parse(module_properties['offline_test'])
    self._classes = np.array(map(int, module_properties['classes'].split(',')))
    self._server_port = module_properties['server_port']
    self._registry = RegistryClient(module_properties['registry'])
    hostname = socket.gethostname()
    address = Utils.get_address(hostname, self._server_port)
    self._stream_client_address = self._registry.reg(ComponentType.LEARNER, address)[0]
    self._handler = LearnerHandler(self._stream_client_address, self._registry, self._parser, self._evaluator, self._dao, self._clf, self._classes, 
                              self._warmup_examples, self._id, self._checkpoint, self._is_prequential, 
                              self._checkpointed, self._offline_test)
    self._processor = StreamService.Processor(self._handler)
    self._stream_server = Server(self._processor, self._server_port, module_properties['multi_threading'])

  def run(self):

    self._stream_server.start()