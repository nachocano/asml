import abc
from scipy import sparse

class Parser:
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def parse_stream(self, fd):
    return

  @abc.abstractmethod
  def parse_raw(self, data):
    return

  def parse_feature(self, N, d, data):
    row = []
    column = []
    value = []
    for i, example in enumerate(data):
      d = example.split(' ')
      label = int(d[0])
      nelems = len(d[1:])
      row.extend([i] * nelems)
      for elem in d[1:]:
        col, val = elem.split(':')
        column.append(col)
        value.append(val)
    return sparse.csr_matrix((value, (row, column)), shape=(N, d))