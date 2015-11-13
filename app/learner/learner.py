import numpy as np
import time

class Learner:
  def __init__(self, config, child, cls):
    self._warmup_batches = int(config['warmup_batches'])
    self._child = child
    self._cls = cls
    self._classes = np.array([0,1])

  def _warmup(self, i):
    return self._warmup_batches > i

  def next(self):
    for i, (X, y) in enumerate(self._child.next()):
      # just train
      if self._warmup(i):
        # update estimator with examples in the current mini-batch
        self._cls.partial_fit(X, y, classes=self._classes)
      else:
        # predict
        predictions = self._cls.predict(X)
        # then train
        self._cls.partial_fit(X, y, classes=self._classes)
        # return predictions and ground truth
        yield i, y, predictions
