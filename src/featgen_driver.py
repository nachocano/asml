#!/usr/bin/python
import argparse

from asml.featgen.feature import FeatureGenerator
from asml.util.utils import Utils

def main():
  parser = argparse.ArgumentParser(description='Feature Generator')
  parser.add_argument('-m', '--module_properties', help='module properties file', required=True)
  args = parser.parse_args()
  module_properties = Utils.read_properties(args.module_properties)
  feature_generator = FeatureGenerator(module_properties)
  feature_generator.run()

if __name__ == '__main__':
  main()