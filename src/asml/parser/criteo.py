from parser import Parser
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from math import factorial
import itertools
import sys
import gzip

class CriteoParser(Parser):
  
  def __init__(self, module_properties):
    Parser.__init__(self)
    self._no_count_feat = 13
    self._no_cat_feat = 26
    self._no_similarity_feat=factorial(self._no_cat_feat)//(factorial(self._no_cat_feat-2)*2)
    # Init target fields
    self.target_fields={'1':'click','0':'noclick'}

    # Init agg dict
    self.dct_agg=defaultdict(float)
    for clicked in self.target_fields.keys():
	for column in range(self._no_count_feat):
            self.dct_agg['Min_'+self.target_fields[clicked]+'_'+str(column)]=0
            self.dct_agg['Count_'+self.target_fields[clicked]+'_'+str(column)]=0
            self.dct_agg['Max_'+self.target_fields[clicked]+'_'+str(column)]=0
            self.dct_agg['Mean_'+self.target_fields[clicked]+'_'+str(column)]=0

    self._no_agg_feat=len(self.dct_agg.keys())

    if module_properties.has_key('hash_dimensions'):
      self._m = int(module_properties['hash_dimensions'])
    if module_properties.has_key('max_mins'):
      maxs_mins = module_properties['max_mins'].split(',')
      self._max_mins = {}
      for i, mm in enumerate(maxs_mins):
        max_, min_ = mm.split(':')
        self._max_mins[i] = (int(max_), int(min_))
      assert len(self._max_mins) == self._no_count_feat

  '''convert to bitfield before calculating similarity'''
  def bitfield(self,n, maxLen=32):
     	lst= [1 if digit=='1' else 0 for digit in bin(n)[2:]]
     	return [0]*(maxLen - len(lst))+lst


  def parse(self, filename):
    features = []
    # send the number of dimensions as the first element
    features.append('%s' % (self._m + self._no_count_feat))
    for i, line in enumerate(gzip.open(filename, 'rb')):
      line = '%s\t%s' % (i, line)
      features.append(self._parse_line(line))
    return self.parse_feature(features)

  def update_summary_aggs(self,count_val,column, clicked):
    self.dct_agg['Min_'+self.target_fields[clicked]+'_'+str(column)]=min(self.dct_agg['Min_'+self.target_fields[clicked]+'_'+str(column)],count_val)
    self.dct_agg['Max_'+self.target_fields[clicked]+'_'+str(column)]=max(self.dct_agg['Max_'+self.target_fields[clicked]+'_'+str(column)],count_val)
    self.dct_agg['Mean_'+self.target_fields[clicked]+'_'+str(column)]=self.dct_agg['Mean_'+self.target_fields[clicked]+'_'+str(column)]* self.dct_agg['Count_'+self.target_fields[clicked]+'_'+str(column)]
    self.dct_agg['Count_'+self.target_fields[clicked]+'_'+str(column)]+=1
   
    

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

    clicked=values[1]
    # count features, normalize them
    counts = []
    for i, count_feature in enumerate(count_features):
      count_val=0
      if count_feature != '':
        as_int = int(count_feature)
        normalized = float(as_int - self._max_mins[i][1]) / (self._max_mins[i][0] - self._max_mins[i][1])
        if normalized < 0:
          normalized == 0
        elif normalized > 1:
          normalized == 1
        counts.append('%s:%s' % (i, normalized))
      	count_val=normalized
	self.update_summary_aggs(count_val,i, clicked)

    # Adding agg features
    aggs=[]
    dct_agg_keys=self.dct_agg.keys()
    for i in range(len(dct_agg_keys)):
	aggs.append('%s:%s' %(i+self._no_count_feat,self.dct_agg[dct_agg_keys[i]])) 

    #print 'Aggs Features', aggs	
    # categorical features, hashed them
    hashed_features = {}
    cat_features_to_hash={} # This is different from the hashed feature as the key in this dictionary will be the original cat column index
    # The cat_features_to_hash index will be between 0 and 25
    for i, cat_feature in enumerate(cat_features):
      if cat_feature != '':
        hashed_key=self._update_feature(cat_feature, 1, hashed_features, self._m)
	cat_features_to_hash[i]=hashed_key
      else:
	cat_features_to_hash[i]=0	
    
    similarities=[]
    cat_features_to_hash_keys=cat_features_to_hash.keys()
    count=0
    for pair in itertools.combinations(cat_features_to_hash_keys,2):
        
	hash1, hash2=self.bitfield(cat_features_to_hash[pair[0]]), self.bitfield(cat_features_to_hash[pair[1]])
	#print 'hash1 {}, hash2 {}'.format(hash1,hash2)
	if hash1==0 or hash2==0:
		similarity=0
	else:
		similarity=cosine_similarity(hash1, hash2)[0][0]
	similarities.append( '%s:%s' %(count+self._no_count_feat+ self._no_agg_feat, similarity))
        count+=1

    #print 'Similarity', similarities
    categories = []

    for key in sorted(hashed_features):
      categories.append('%s:%s' % (key + self._no_count_feat+self._no_agg_feat+self._no_similarity_feat, hashed_features[key]))
    
    #print 'Categories', categories
    counts_as_str = ' '.join(count_f for count_f in counts)
    categories_as_str = ' '.join(c for c in categories)
    aggs_as_str=  ' '.join(agg_f for agg_f in aggs)
    sims_as_str= ' '.join(sim_f for sim_f in similarities)
    # timestamp, label, count_features, categorical_features
    parsed_line = '%s %s %s %s %s %s' % (values[0], values[1], counts_as_str, categories_as_str, aggs_as_str, sims_as_str)
    #print 'parsed_line', parsed_line
    #sys.exit(-1)
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
    return hashed_key





