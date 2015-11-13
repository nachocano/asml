#!/usr/bin/python
import argparse
import yaml
from app.pipeline import Pipeline
from app.stream.file import FileStream
from app.learner.sgd import SGD
from app.learner.pa import PA
from app.predict.predictor import Predictor
from app.eval.auc import AUC



def main():
  parser = argparse.ArgumentParser(description='Self-Tunning Machine Learning')
  parser.add_argument('-c', '--config_file', help='configuration file', required=True) 
  args = parser.parse_args()
  with open(args.config_file) as f:
    config = yaml.load(f)

  # for now we assume is a file, if time, we can support data
  # coming from a socket
  data_stream = FileStream(config)
  # evaluator
  eval = config['eval']
  if eval == 'auc':
    evaluator = AUC()
  else:
    evaluator = RMSE()

  # either learn or predict
  mode = config['mode']
  if mode == 'learn':
    # SGD based classifier
    if config['learner'] == 'sgd':
      module = SGD(config, data_stream)
    # or Passive Aggressive based classifier
    else:
      module = PA(config, data_stream)
  else:
    module = Predictor(config, data_stream)
  

  evaluator.set_child(module)

  # run the ML pipeline
  pipeline = Pipeline(evaluator)
  pipeline.run()
  
if __name__ == '__main__':
  main()

