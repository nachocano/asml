'''
Passive Aggresive Classifier
'''
from sklearn.linear_model import PassiveAggressiveClassifier
import numpy as np
import time

class PA:

  def __init__(self, config, child):
    self._child = child
    self._cls = PassiveAggressiveClassifier(C=config['C'], loss=config['loss'])
    print self._cls

  def next(self):
    for i, (X_train, y_train) in enumerate(self._child.iter_minibatches()):
      print i
      tick = time.time()
      # update estimator with examples in the current mini-batch
      self._cls.partial_fit(X_train, y_train, classes=np.array([0,1]))
      print 'time %s for it %d' % (time.time() - tick, i)
