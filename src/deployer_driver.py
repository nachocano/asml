#!/usr/bin/python
import argparse
from asml.deploy.deployer import Deployer
from asml.util.utils import Utils

def main():
  parser = argparse.ArgumentParser(description='Deployer')
  parser.add_argument('-m', '--module_properties', help='module properties file', required=True)
  args = parser.parse_args()
  
  module_properties = Utils.read_properties(args.module_properties)
  
  deployer = Deployer(module_properties)
  deployer.run()

if __name__ == '__main__':
  main()

