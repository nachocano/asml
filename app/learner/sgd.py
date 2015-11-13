'''
SGD classifer
'''
from sklearn.linear_model import SGDClassifier
from learner import Learner

class SGD(Learner):
  def __init__(self, config, child):
    Learner.__init__(self, config, child, SGDClassifier(loss=config['loss'], penalty=config['penalty'],
                   learning_rate=config['step_policy'], eta0=config['eta0'], average=config['average']))
