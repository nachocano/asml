
from pa import PA
from sgd import SGD

class LearnerFactory:

  @classmethod
  def new_learner(cls, module_properties, dao):
    learner = module_properties['learner']
    if learner == 'sgd':
      return SGD(module_properties, dao)
    elif learner == 'pa':
      return PA(module_properties, dao)
    else:
      raise ValueException('invalid learner %s' % learner)