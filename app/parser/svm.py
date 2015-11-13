
class SVMLightParser:
  
  def parse(self, fd):
    for line in fd:
      values = line.split()
      y = int(values[0])
      # TODO, change this, the dataset will be sparse
      X = [float(v.split(':')[1]) for v in values[1:]]
      yield X, y