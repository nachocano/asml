from asml.util.utils import Utils
from asml.autogen.asml import StreamService
from asml.network.server import StreamServer

class DeployerHandler:
  def __init__(self):
    self._count = 0

  def emit(self, data):
    print data
    self._count += 1
    print 'count %d' % self._count

class Deployer:
  def __init__(self, module_properties):
    self._processor = StreamService.Processor(DeployerHandler())
    self._stream_server = StreamServer(module_properties, self._processor)


  def run(self):
    self._stream_server.start()
    # for tup in self._child.next():
    #   epoch = tup[0]
    #   clf = tup[1]
    #   timestamp = (epoch + 1) * self._batch_size
    #   if Utils.warmup(self._warmup_batches, epoch):
    #     epoch, clf = tup
    #     timestamp = (epoch + 1) * self._batch_size
    #     self._save_model(timestamp, clf)
    #   else:
    #     y = tup[2]
    #     preds = tup[3]
    #     timestamp = (epoch + 1) * self._batch_size
    #     new_eval = self._evaluator.stream_eval(y, preds)
    #     if self._evaluator.is_better(new_eval, self._current_eval):
    #       self._current_eval = new_eval
    #       self._save_model(timestamp, clf)
    #       print 'better accuracy %s' % self._current_eval
    #     else:
    #       print 'not better...'