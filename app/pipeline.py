
class Pipeline:
  def __init__(self, child):
    self._child = child

  def run(self):
    print 'running pipeline...'
