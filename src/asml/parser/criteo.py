from parser import Parser
import gzip

class CriteoParser(Parser):
  
  def __init__(self, module_properties):
    Parser.__init__(self)
    self._no_count_feat = 13
    self._no_cat_feat = 26
    if module_properties.has_key('hash_dimensions'):
      self._m = int(module_properties['hash_dimensions'])
    if module_properties.has_key('max_mins'):
      maxs_mins = module_properties['max_mins'].split(',')
      self._max_mins = {}
      for i, mm in enumerate(maxs_mins):
        max_, min_ = mm.split(':')
        self._max_mins[i] = (int(max_), int(min_))
      assert len(self._max_mins) == self._no_count_feat

  def parse(self, filename):
    features = []
    # send the number of dimensions as the first element
    features.append('%s' % (self._m + self._no_count_feat))
    for i, line in enumerate(gzip.open(filename, 'rb')):
      line = '%s\t%s' % (i, line)
      features.append(self._parse_line(line))
    return self.parse_feature(features)

  def parse_stream(self, fd):
    for i, line in enumerate(fd):
      yield '%s\t%s' % (i, line)

  def parse_raw(self, data):
    features = []
    # send the number of dimensions as the first element
    features.append('%s' % (self._m + self._no_count_feat))
    for line in data:
      features.append(self._parse_line(line))
    return features

  def _parse_line(self, line):
    values = self._get_values(line)
    # 0 = timestamp
    # 1 = label
    # [2:15] count features (13)
    count_features = values[2:self._no_count_feat+2]
    # [15:] categorical features (26)
    cat_features = values[self._no_count_feat+2:]

    # count features, normalize them
    counts = []
    for i, count_feature in enumerate(count_features):
      if count_feature != '':
        as_int = int(count_feature)
        normalized = float(as_int - self._max_mins[i][1]) / (self._max_mins[i][0] - self._max_mins[i][1])
        if normalized < 0:
          normalized == 0
        elif normalized > 1:
          normalized == 1
        counts.append('%s:%s' % (i, normalized))

    # categorical features, hashed them
    hashed_features = {}
    for i, cat_feature in enumerate(cat_features):
      if cat_feature != '':
        self._update_feature(cat_feature, 1, hashed_features, self._m)
    categories = []
    for key in sorted(hashed_features):
      categories.append('%s:%s' % (key + self._no_count_feat, hashed_features[key]))
    
    counts_as_str = ' '.join(count_f for count_f in counts)
    categories_as_str = ' '.join(c for c in categories)
    # timestamp, label, count_features, categorical_features
    parsed_line = '%s %s %s %s' % (values[0], values[1], counts_as_str, categories_as_str)
    return parsed_line

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






