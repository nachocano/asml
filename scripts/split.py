import argparse
import gzip

parser = argparse.ArgumentParser(description='ASML Split')
parser.add_argument('-i', '--input_file', required=True, help="the input file")
parser.add_argument('-t', '--train_instances', type=int, required=True, help="train instances")
parser.add_argument('-otr', '--output_train', required=True, help="the output train file")
parser.add_argument('-ot', '--output_test', required=True, help="the output test file")
args = parser.parse_args()

def read_lines(f):
  for ii,line in enumerate(f):
    yield ii, line

otr = gzip.open(args.output_train, 'w')
ot = gzip.open(args.output_test, 'w')

with gzip.open(args.input_file, 'r') as f:
  for ii, line in read_lines(f):
    if ii % 100000 == 0:
      print 'processing %s' % ii
    if ii < args.train_instances:
      otr.write(line)
    else:
      ot.write(line)

otr.close()
ot.close()