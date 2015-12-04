import abc
from scipy import sparse
import numpy as np

class Parser:
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def parse_stream(self, fd):
    return

  @abc.abstractmethod
  def parse_raw(self, data):
    return

  def parse_feature(self, data):
    labels, row, column, value = [], [], [], []
    timestamp = -1
    N = len(data) - 1
    d = int(data[0])
    for i in xrange(1,len(data)):
      example = data[i].split(' ')
      timestamp = long(example[0])
      labels.append(int(example[1]))
      nelems = len(example[2:])
      row.extend([i-1] * nelems)
      for elem in example[2:]:
        col, val = elem.split(':')
        column.append(int(col))
        value.append(int(val))
    X = sparse.csr_matrix((value, (row, column)), shape=(len(data)-1, d))
    y = np.array(labels)
    return X, y, timestamp