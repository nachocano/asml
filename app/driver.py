#!/usr/bin/python
import argparse
import yaml
from app.pipeline import Pipeline
from app.stream.file import FileStream
from app.learner.sgd import SGD
from app.learner.pa import PA
from app.predict.predictor import Predictor
from app.eval.auc import AUC
from app.eval.accuracy import Accuracy
from app.dao.database import DB
from app.deploy.deployer import Deployer
from app.cache.rediscache import RedisCache
from app.reaper.task import ReaperTask

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

  dao = DB(app_properties, conn_properties, sql_statements)
  reaper_task = ReaperTask(dao)

  # for now we assume is a file, if time, we can support data
  # coming from a socket
  data_stream = FileStream(app_properties)
  # evaluator
  eval = app_properties['eval']
  if eval == 'accuracy':
    evaluator = Accuracy()
  else:
    evaluator = AUC()
  # cache
  cache = RedisCache(conn_properties)

  # either learn or predict
  mode = app_properties['mode']
  if mode == 'learn':
    # SGD based classifier
    if app_properties['learner'] == 'sgd':
      learner = SGD(app_properties, data_stream)
    # or Passive Aggressive based classifier
    else:
      learner = PA(app_properties, data_stream)
    # create the deployer
    module = Deployer(app_properties, cache, dao, evaluator, learner)

  else:
    module = Predictor(app_properties, cache, dao, evaluator, data_stream)
  

  # run the ML pipeline
  pipeline = Pipeline(module)
  pipeline.run()
  
if __name__ == '__main__':
  main()

