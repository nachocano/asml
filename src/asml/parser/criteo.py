from parser import Parser

class CriteoParser(Parser):
  
  def __init__(self, m=100000):
    Parser.__init__(self)
    self._no_count_feat = 13
    self._no_cat_feat = 26
    self._m = m

  def parse_stream(self, fd):
    for i, line in enumerate(fd):
      yield '%s\t%s' % (i, line)

  def parse_raw(self, data):
    features = []
    for line in data:
      values = self._get_values(line)
      # 0 = timestamp
      # 1 = label
      # [2:15] count features (13)
      count_features = values[2:self._no_count_feat+2]
      # [15:] categorical features (26)
      cat_features = values[self._no_count_feat+2:]

      hashed_features = {}
      for i, cat_feature in enumerate(cat_features):
        if cat_feature != '':
          self._update_feature(cat_feature, 1, hashed_features, self._m)

      categories = []
      for key in sorted(hashed_features):
        categories.append('%s:%s' % (key, hashed_features[key]))
      categories_as_str = ' '.join(c for c in categories)
      # timestamp, label, categories
      features.append('%s %s %s' % (values[0], values[1], categories_as_str))
    return features

  def _get_values(self, line):
    values = line.split('\t')
    # remove \n if it's at the end, or if \n is the last element, remove it as well
    if '\n' in values[-1]:
      values[-1] = values[-1].replace('\n','')
    elif values[-1] == '\n':
      values = values[:-1]
    # i, label, 13 counts, 26 categorical
    assert len(values) == 41
    return values

  # hashing utilities (ML4BD class)

  def _hash_to_range(self, s, upper):
    hashval = hash(str(s)) % upper;
    if hashval < 0:
      hashval = upper + hashval
    return hashval

  def _hash_to_sign(self, s):
    if hash(str(s)) % 2 == 0:
      return -1
    else:
      return 1

  def _update_feature(self, key, val, hashed_features, dim):
    hashed_key = self._hash_to_range(key, dim)
    hashed_sign = self._hash_to_sign(key)
    current_hashed_value = hashed_features.get(hashed_key, 0)
    current_hashed_value += val * hashed_sign
    hashed_features[hashed_key] = current_hashed_value






