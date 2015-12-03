#!/usr/bin/python
import argparse
import os
import subprocess

def main():
  parser = argparse.ArgumentParser(description='Runner')
  parser.add_argument('-e', '--executable', required=True)
  parser.add_argument('-a', '--app_resources_folder', required=True)
  parser.add_argument('-c', '--connection_file', required=True)
  parser.add_argument('-s', '--sql_statements_file', required=True)
  args = parser.parse_args()
  for name in os.listdir(args.app_resources_folder):
    fn = os.path.join(args.app_resources_folder, name)
    if os.path.isfile(fn) and not name.startswith('.'):
      cmd = 'python %s -a %s -c %s -s %s' % (args.executable, fn, args.connection_file, args.sql_statements_file)
      print cmd
      subprocess.Popen(cmd, shell=True)
      break
   
if __name__ == '__main__':
  main()
