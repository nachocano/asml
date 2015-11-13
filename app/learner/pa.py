'''
Passive Aggresive Classifier
'''
from sklearn.linear_model import PassiveAggressiveClassifier

class PA:
  def __init__(self, config, child):
    self._child = child
    self._cls = PassiveAggressiveClassifier(C=config['C'], loss=config['loss'])
    print self._cls
