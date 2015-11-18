import numpy as np
import time
from app.util.utils import Utils

class Learner:
  def __init__(self, app_properties, child, clf):
    self._warmup_batches = app_properties['warmup_batches']
    self._child = child
    self._clf = clf
    self._classes = np.array(map(int, app_properties['classes'].split(',')))

  def next(self):
    for i, (X, y) in enumerate(self._child.next()):
      # just train
      if Utils.warmup(self._warmup_batches, i):
        # train
        self._clf.partial_fit(X, y, classes=self._classes)
        yield i, self._clf
      else:
        # predict
        predictions = self._clf.predict(X)
        # then train
        self._clf.partial_fit(X, y, classes=self._classes)
        # return ground truth, predictions and model
        yield i, self._clf, y, predictions
