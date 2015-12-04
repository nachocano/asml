#!/usr/bin/python
import argparse
from asml.learner.sgd import SGD
from asml.learner.pa import PA
from asml.util.utils import Utils

def main():
  parser = argparse.ArgumentParser(description='Learner')
  parser.add_argument('-m', '--module_properties', help='module properties file', required=True)
  args = parser.parse_args()
  module_properties = Utils.read_properties(args.module_properties)
  if module_properties['learner'] == 'sgd':
    learner = SGD(module_properties)
  else:
    learner = PA(module_properties)

  learner.run()

if __name__ == '__main__':
  main()

