import abc
from scipy import sparse
import numpy as np
import gzip

class Parser:
  __metaclass__ = abc.ABCMeta


  @abc.abstractmethod
  def num_features(self):
    return

  @abc.abstractmethod
  def parse_line(self, line):
    return

  # for holdout testing data
  def parse(self, filename):
    features = []
    # send the number of dimensions as the first element
    features.append('%s' % (self._m + self._no_count_feat))
    for i, line in enumerate(gzip.open(filename, 'rb')):
      line = '%s\t%s' % (i, line)
      features.append(self.parse_line(line))
    return self.parse_feature(features)

  # adds the timestamp
  def parse_stream(self, fd):
    for i, line in enumerate(fd):
      yield '%s\t%s' % (i, line)

  # generates the features from raw data
  def parse_raw(self, data):
    features = []
    # send the number of dimensions as the first element
    features.append('%s' % self.num_features())
    for line in data:
      features.append(self.parse_line(line))
    return features

  # features into numpy formats
  def parse_feature(self, data):
    timestamps, labels, row, column, value = [], [], [], [], []
    N = len(data) - 1
    d = int(data[0])
    for i in xrange(1,len(data)):
      example = data[i].split(' ')
      timestamps.append(long(example[0]))
      labels.append(int(example[1]))
      nelems = len(example[2:])
      row.extend([i-1] * nelems)
      for elem in example[2:]:
        col, val = elem.split(':')
        column.append(int(col))
        value.append(float(val))
    X = sparse.csr_matrix((value, (row, column)), shape=(len(data)-1, d))
    y = np.array(labels)
    timestamps = np.array(timestamps)
    return X, y, timestamps