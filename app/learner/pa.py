'''
Passive Aggresive Classifier
'''
from sklearn.linear_model import PassiveAggressiveClassifier
from learner import Learner

class PA(Learner):

  def __init__(self, config, child):
    Learner.__init__(self, config, child, PassiveAggressiveClassifier(C=config['C'], loss=config['loss'], shuffle=False))