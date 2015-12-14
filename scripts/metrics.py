import string
import argparse
import numpy as np
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import zero_one_loss
from sklearn.metrics import log_loss
import math

parser = argparse.ArgumentParser(description='ASML metrics')
parser.add_argument('-i', '--input_file', required=True, help="the input file")
args = parser.parse_args()

def read_lines(f):
  for ii,line in enumerate(f):
    yield ii, line

def to_int(x):
  return round(x)

rmses, timestamps, truths, preds = [], [], [], []
with open(args.input_file, 'r') as f:
  for ii, line in read_lines(f):
    if ii % 1000000 == 0:
      print 'processed %s' % ii
    line = line.splitlines()[0].split(' ')
    if len(line) == 1:
      time, rmse = line[0].split(':')
      rmses.append(float(rmse))
    if len(line) == 3:
      timestamps.append(long(line[0]))
      truths.append(int(line[1]))
      preds.append(float(line[2]))

truths = np.array(truths)
preds = np.array(preds)

wmse = 0.0
for i, t in enumerate(truths):
  wmse += pow((t - preds[i]), 2)
print 'rmse %s' % math.sqrt(wmse / truths.shape[0])
print 'avg rmse %s' % (sum(rmses)/len(rmses))
print 'log loss %s' % log_loss(truths, preds)
fpr, tpr, _ = roc_curve(truths, preds)
print 'auc %s' % auc(fpr, tpr)
int_preds = map(to_int, preds)
print '0/1 %s' % zero_one_loss(truths, int_preds, normalize=False)