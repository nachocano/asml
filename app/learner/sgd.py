'''
SGD classifer
'''
from sklearn.linear_model import SGDClassifier

class SGD:
  def __init__(self, config, child):
    self._child = child
    self._cls = SGDClassifier(loss=config['loss'], penalty=config['penalty'], learning_rate=config['step_policy'],
                             eta0=config['eta0'], average=config['average'])
    print self._cls
