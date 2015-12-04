'''
Passive Aggresive Classifier
'''
from sklearn.linear_model import PassiveAggressiveClassifier
from learner import Learner

class PA(Learner):

  def __init__(self, module_properties):
    Learner.__init__(self, module_properties, PassiveAggressiveClassifier(C=module_properties['C'], 
                    loss=module_properties['loss'], shuffle=False))