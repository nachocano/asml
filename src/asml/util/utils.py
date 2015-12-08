import yaml
import base64
try:
  import cPickle as pickle
except:
  import pickle

class Utils:

  @classmethod
  def read_properties(cls, fd):
    with open(fd) as f:
      return yaml.load(f)

  @classmethod
  def serialize(cls, object):
    try:
      return base64.b64encode(pickle.dumps(object, pickle.HIGHEST_PROTOCOL))
    except Exception, ex:
      print 'exc serializing %s' % ex.message


  @classmethod
  def deserialize(cls, string):
    try:
      return pickle.loads(base64.b64decode(string))
    except Exception, ex:
      print 'exc deserializing %s' % ex.message