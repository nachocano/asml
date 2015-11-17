import base64
try:
  import cPickle as pickle
except:
  import pickle

class Serializer:

  @classmethod
  def serialize(cls, object):
    return base64.b64encode(pickle.dumps(object, pickle.HIGHEST_PROTOCOL))


  @classmethod
  def deserialize(cls, string):
    return pickle.load(base64.b64decode(string))
