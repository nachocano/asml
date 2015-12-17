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

  @classmethod
  def get_address(cls, host, port):
    return '%s:%s' % (host, port)

  @classmethod
  def get_address_components(cls, address):
    host, port = address.split(':')
    port = int(port)
    return host, port

  @classmethod
  def diff(cls, list1, list2):
    c = set(list1).union(set(list2))
    d = set(list1).intersection(set(list2))
    return list(c - d)

  # hashing utilities (ML4BD class)
  
  @classmethod
  def hash_to_range(cls, s, upper):
    hashval = hash(str(s)) % upper;
    if hashval < 0:
      hashval = upper + hashval
    return hashval

  @classmethod
  def hash_to_sign(cls, s):
    if hash(str(s)) % 2 == 0:
      return -1
    else:
      return 1
  
  @classmethod
  def update_feature(cls, key, val, hashed_features, dim):
    hashed_key = Utils.hash_to_range(key, dim)
    hashed_sign = Utils.hash_to_sign(key)
    current_hashed_value = hashed_features.get(hashed_key, 0)
    current_hashed_value += val * hashed_sign
    hashed_features[hashed_key] = current_hashed_value
