import numpy as np
import time
from app.model.serializer import Serializer

class Learner:
  def __init__(self, app_properties, dao, child, clf):
    self._warmup_batches = app_properties['warmup_batches']
    self._name = app_properties['name']
    self._dao = dao
    self._child = child
    self._clf = clf
    self._classes = np.array(map(int, app_properties['classes'].split(',')))

  def _warmup(self, i):
    return self._warmup_batches > i

  def _save_model(self, i):
    self._dao.save_model(i, self._name, Serializer.serialize(self._clf))

  def next(self):
    for i, (X, y) in enumerate(self._child.next()):
      # just train
      if self._warmup(i):
        # update estimator with examples in the current mini-batch
        self._clf.partial_fit(X, y, classes=self._classes)
        self._save_model(i)
      else:
        # predict
        predictions = self._clf.predict(X)
        # then train
        self._clf.partial_fit(X, y, classes=self._classes)
        self._save_model(i)
        # return predictions and ground truth
        yield i, y, predictions
