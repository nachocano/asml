#http://www.kddcup2012.org/c/kddcup2012-track2
from sklearn.metrics.pairwise import cosine_similarity
import sys
import csv
HASH_LENGTH=2
# length of the hash is going to be logm*8 bits
def hashing(vector, m=HASH_LENGTH):

	feature_vector=[0 for _ in xrange(1<<m)]
	for token in vector.split('|'):
		hashed_token=hash(token)
		index = hashed_token & ((1 << m) - 1)
		sign = (((hashed_token & (1 << m)) >> m) << 1) - 1
		feature_vector[index]+=sign
	return feature_vector

def readFile(filename):
	header=['click','impression','displayURL','AdId','AdvertiserId','Depth','Position','QueryId','KeywordId','TitleId','DescriptionId','UserId','Gender','Age','QueryTokens','DescriptionTokens','KeywordTokens','TitleTokens']
	row_dict={}
	with open(filename,'r') as fin:
		line_count=0
		csv_r=csv.reader(fin)
		for row in csv_r:
			#print row	
			if line_count==0:
				print 'Header Read'
				line_count+=1
			else:
				dct={}						
				for i in range(len(row)):
					dct[header[i]]=row[i]	
				hashable_fields=['QueryTokens','DescriptionTokens','KeywordTokens','TitleTokens']
				for i in range(len(hashable_fields)):
				   for j in range(i+1, len(hashable_fields)):
					field1=dct[hashable_fields[i]]
					field2=dct[hashable_fields[j]]
					hash1=hashing(field1)
					hash2=hashing(field2)
					similarity=cosine_similarity(hash1, hash2)[0][0]
					#print 'similarity_'+str(hashable_fields[i])+'_'+str(hashable_fields[j])
					dct['similarity_'+str(hashable_fields[i])+'_'+str(hashable_fields[j])]=similarity								
				row_dict[line_count-1]=dct# Accounting for header
				line_count+=1
	
	fout=open('out.txt','w')
	strout=','.join(each  for each in row_dict[0].keys())
	fout.write(strout+'\n')
	for each in row_dict:
		dct=row_dict[each]
		print dct
		strout=','.join(str(dct[each]) for each in dct)
		fout.write(strout+'\n')
	fout.close()
if __name__=='__main__':
	readFile(sys.argv[1])
