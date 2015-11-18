'''
Passive Aggresive Classifier
'''
from sklearn.linear_model import PassiveAggressiveClassifier
from learner import Learner

class PA(Learner):

  def __init__(self, app_properties, child):
    Learner.__init__(self, app_properties, child, PassiveAggressiveClassifier(C=app_properties['C'], 
                    loss=app_properties['loss'], shuffle=False))