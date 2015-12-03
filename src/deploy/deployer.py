from app.util.utils import Utils
from app.model.serializer import Serializer

class Deployer:
  def __init__(self, app_properties, cache, dao, evaluator, child):
    self._warmup_batches = app_properties['warmup_batches']
    self._batch_size = app_properties['batch_size']
    self._name = app_properties['name']
    self._cache = cache
    self._dao = dao
    self._evaluator = evaluator
    self._child = child
    self._current_eval = self._evaluator.default()

  def _save_model(self, timestamp, clf):
    self._dao.save_model(timestamp, self._name, Serializer.serialize(clf), self._current_eval)

  def next(self):
    for tup in self._child.next():
      epoch = tup[0]
      clf = tup[1]
      timestamp = (epoch + 1) * self._batch_size
      if Utils.warmup(self._warmup_batches, epoch):
        epoch, clf = tup
        timestamp = (epoch + 1) * self._batch_size
        self._save_model(timestamp, clf)
      else:
        y = tup[2]
        preds = tup[3]
        timestamp = (epoch + 1) * self._batch_size
        new_eval = self._evaluator.stream_eval(y, preds)
        if self._evaluator.is_better(new_eval, self._current_eval):
          self._current_eval = new_eval
          self._save_model(timestamp, clf)
          print 'better accuracy %s' % self._current_eval
        else:
          print 'not better...'