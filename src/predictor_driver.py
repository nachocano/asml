#!/usr/bin/python
import logging
import argparse
from asml.dao.database import DB
from asml.predict.predictor import Predictor
from asml.util.utils import Utils

def main():
  parser = argparse.ArgumentParser(description='Learner')
  parser.add_argument('-m', '--module_properties', help='module properties file', required=True)
  parser.add_argument('-d', '--db_properties', help='database connection properties file', required=True)
  parser.add_argument('-s', '--sql_statements', help='sql statements file', required=True)
  args = parser.parse_args()
  
  module_properties = Utils.read_properties(args.module_properties)
  db_properties = Utils.read_properties(args.db_properties)
  sql_statements = Utils.read_properties(args.sql_statements)

  logging.basicConfig(filename=module_properties['log_file'], format='%(asctime)s %(message)s', level=logging.DEBUG)

  dao = DB(db_properties, sql_statements)

  predictor = Predictor(module_properties, dao)
  predictor.run()

  #reaper_task = ReaperTask(dao)

if __name__ == '__main__':
  main()