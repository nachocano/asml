#!/usr/bin/python
import argparse
import yaml
from app.pipeline import Pipeline
from app.stream.file import FileStream
from app.learner.sgd import SGD
from app.learner.pa import PA
from app.predict.predictor import Predictor
from app.eval.auc import AUC
from app.eval.rmse import RMSE
from app.dao.database import DB

def read_properties(fd):
  with open(fd) as f:
    return yaml.load(f)  

def main():
  parser = argparse.ArgumentParser(description='Self-Tunning Machine Learning')
  parser.add_argument('-a', '--app_properties', help='application properties file', required=True)
  parser.add_argument('-c', '--connection_properties', help='connection properties file', required=True)
  parser.add_argument('-s', '--sql_statements', help='sql statements file', required=True)
  args = parser.parse_args()

  app_properties = read_properties(args.app_properties)
  conn_properties = read_properties(args.connection_properties)
  sql_statements = read_properties(args.sql_statements)

  dao = DB(conn_properties, sql_statements)

  # for now we assume is a file, if time, we can support data
  # coming from a socket
  data_stream = FileStream(app_properties)
  # evaluator
  eval = app_properties['eval']
  if eval == 'auc':
    evaluator = AUC()
  else:
    evaluator = RMSE()

  # either learn or predict
  mode = app_properties['mode']
  if mode == 'learn':
    # SGD based classifier
    if app_properties['learner'] == 'sgd':
      module = SGD(app_properties, dao, data_stream)
    # or Passive Aggressive based classifier
    else:
      module = PA(app_properties, dao, data_stream)
  else:
    module = Predictor(app_properties, data_stream)
  

  evaluator.set_child(module)

  # run the ML pipeline
  pipeline = Pipeline(evaluator)
  pipeline.run()
  
if __name__ == '__main__':
  main()

