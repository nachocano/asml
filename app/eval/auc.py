
class AUC:
  def __init__(self):
    self._child = None

  @property
  def child(self):
    return self._child

  @child.setter
  def child(self, value):
    self._child = value

  def run(self):
    pass
