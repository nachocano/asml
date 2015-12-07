import argparse
import time
from collections import defaultdict
import os
import gzip

parser = argparse.ArgumentParser(description='Max-Mins of Criteo dataset')
parser.add_argument('-t', '--input_folder', required=True, help="the input train folder")
args = parser.parse_args()

def read_lines(f):
  for ii,line in enumerate(f):
    yield ii, line

def get_values(line):
  values = line.split('\t')
  # remove \n if it's at the end, or if \n is the last element, remove it as well
  if '\n' in values[-1]:
    values[-1] = values[-1].replace('\n','')
  elif values[-1] == '\n':
    values = values[:-1]
  return values

num_int_features = 13
integer_features_max = defaultdict(lambda : -9999)
integer_features_min = defaultdict(lambda: 9999)

for fi in os.listdir(args.input_folder):
    if not fi.endswith('.gz'):
      continue
    gzipped = os.path.join(args.input_folder, fi)
    f = gzip.open(gzipped, 'r')
    start = time.time()
    print 'processing file %s' % f
    for ii, line in read_lines(f):
      if ii % 100000 == 0:
        print "processing %d of file %s" % (ii, gzipped)
      values = get_values(line)
      i_features = None
      # have the labels
      assert len(values) == 40
      i_features = values[1:num_int_features+1]
      # 13 categorical features
      assert len(i_features) == num_int_features
      for i, i_feat in enumerate(i_features):
        if i_feat != '':
          if int(i_feat) > integer_features_max[i]:
            integer_features_max[i] = int(i_feat)
          if int(i_feat) < integer_features_min[i]:
            integer_features_min[i] = int(i_feat)
    print 'file %s processed in %s' % (fi, time.time() - start)

print "max and mins..."
for i in xrange(num_int_features):
  print integer_features_max[i], integer_features_min[i]
