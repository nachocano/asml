#!/usr/bin/python
import argparse

from asml.stream.file import FileStream
from asml.util.utils import Utils

def main():
  parser = argparse.ArgumentParser(description='Data Stream')
  parser.add_argument('-m', '--module_properties', help='module properties file', required=True)
  args = parser.parse_args()
  module_properties = Utils.read_properties(args.module_properties)
  data_stream = FileStream(module_properties)
  data_stream.run()

if __name__ == '__main__':
  main()

