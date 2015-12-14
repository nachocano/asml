from __future__ import division
import argparse
import os
import pandas
from ggplot import *

parser = argparse.ArgumentParser(description='ASML Plotter')
parser.add_argument('-i', '--input', required=True, help='input folder where the files are')
args = parser.parse_args()

def read_lines(f):
  for ii,line in enumerate(f):
    yield ii, line

dd = pandas.DataFrame()
for f in os.listdir(args.input):
  if not f.endswith('.log'):
      continue
  fi = os.path.join(args.input, f)
  key = fi[fi.rfind('/')+1:fi.rfind('.')]
  print 'processing %s' % fi
  df = pandas.DataFrame()
  with open(fi, 'r') as f:
    times = []
    rmses = []
    for ii, line in read_lines(f):
      if ii % 1000000 == 0:
        print ' processed %s' % ii
      line = line.splitlines()[0].split(' ')
      if len(line) == 1:
        time, rmse = line[0].split(':')
        times.append(int(time))
        rmses.append(float(rmse))
    df['times'] = times
    df['rmses'] = rmses
    df['method'] = key
  dd = dd.append(df)

dd.to_csv('data.csv')





    