#!/usr/bin/python
import argparse
from asml.register.registry import Registry
from asml.util.utils import Utils

def main():
  parser = argparse.ArgumentParser(description='Registry')
  parser.add_argument('-m', '--module_properties', help='module properties file', required=True)
  args = parser.parse_args()
  
  module_properties = Utils.read_properties(args.module_properties)
  
  registry = Registry(module_properties)
  registry.run()

if __name__ == '__main__':
  main()

