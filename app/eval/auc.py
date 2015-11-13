
class AUC:
  def __init__(self):
    self._child = None

  def set_child(self, value):
    self._child = value

  def next(self):
    self._child.next()
