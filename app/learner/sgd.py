'''
SGD classifer
'''
from sklearn.linear_model import SGDClassifier
from learner import Learner

class SGD(Learner):
  def __init__(self, app_properties, dao, child):
    Learner.__init__(self, app_properties, dao, child, SGDClassifier(loss=app_properties['loss'], penalty=app_properties['penalty'],
                    learning_rate=app_properties['step_policy'], eta0=app_properties['eta0'], average=app_properties['average'],
                    shuffle=False))
