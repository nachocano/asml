from parser import Parser
from asml.util.utils import Utils

class KddParser(Parser):
  
  def __init__(self, module_properties):
    Parser.__init__(self)
    if module_properties.has_key('hash_dimensions'):
      self._m = int(module_properties['hash_dimensions'])
      self._regular_features = 4
      
  def num_features(self):
    return self._m + self._regular_features

  def parse_line(self, line):
    # remove \n
    line = line.splitlines()[0]
    timestamp, rest = line.split('\t')
    fields = rest.split("|")
    clicked = int(fields[0])
    # depth of the session
    depth = int(fields[1])
    position = int(fields[2])
    userid = int(fields[3])
    # user gender indicator (-1 for male, 1 for female)
    gender = int(fields[4])
    if gender != 0:
      gender = int((gender - 1.5) * 2)
    # user age indicator:
    #   '1' for (0, 12],
    #   '2' for (12, 18],
    #   '3' for (18, 24],
    #   '4' for (24, 30],
    #   '5' for (30, 40], and
    #   '6' for greater than 40.
    age = int(fields[5])
    # list of token ids
    tokens = [int(xx) for xx in fields[6].split(",")]
    
    # hash tokens
    hashed_tokens = {}
    for i, token in enumerate(tokens):
      Utils.update_feature(token, 1, hashed_tokens, self._m)
      if userid > 0:
        user_token = str(token) + "_" + str(userid)
        Utils.update_feature(user_token, 1, hashed_tokens, self._m)

    hashed_tokens_arr = []
    for key in sorted(hashed_tokens):
      hashed_tokens_arr.append('%s:%s' % (key + self._regular_features, hashed_tokens[key]))
    
    tokens_as_str = ' '.join(token_f for token_f in hashed_tokens_arr)
    # timestamp, label, depth, position, gender, age, categorical_features
    parsed_line = '%s %s 0:%s 1:%s 2:%s 3:%s %s' % (timestamp, clicked, depth, position, gender, age, tokens_as_str)
    return parsed_line
