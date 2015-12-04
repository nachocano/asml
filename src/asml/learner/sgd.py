'''
SGD classifer
'''
from sklearn.linear_model import SGDClassifier
from learner import Learner

class SGD(Learner):
  def __init__(self, module_properties, dao):
    Learner.__init__(self, module_properties, dao, SGDClassifier(loss=module_properties['loss'], penalty=module_properties['penalty'],
                    learning_rate=module_properties['step_policy'], eta0=module_properties['eta0'], average=module_properties['average'],
                    shuffle=False))
