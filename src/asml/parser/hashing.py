from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
import sys
import csv
import numpy as np

## GLOBALS

HASH_LENGTH=2
num_count_features=13
num_categorical_features=26
##

'''
Hashing Function
Note: length of the hash is going to be logm*8 bits
'''
def hashing(vector, m=HASH_LENGTH):

    feature_vector=[0 for _ in xrange(1<<m)]
    for token in vector.split('|'):
        hashed_token=hash(token)
        index = hashed_token & ((1 << m) - 1)
        sign = (((hashed_token & (1 << m)) >> m) << 1) - 1
        feature_vector[index]+=sign
    return feature_vector


'''Function to init aggregate dictionary'''
def init_agg_dict(target_fields, count_fields):
    dct_agg=defaultdict(float) #dictionary for aggregate measures 
    #initializing the dct_agg so that every output row has all the columns
    for clicked in target_fields.keys():
        for column in count_fields:
            dct_agg['Min_'+target_fields[clicked]+'_'+column]=0
            dct_agg['Count_'+target_fields[clicked]+'_'+column]=0
            dct_agg['Max_'+target_fields[clicked]+'_'+column]=0
            dct_agg['Mean_'+target_fields[clicked]+'_'+column]=0
    return dct_agg


'''Function to update summary stats in the aggregate dictionary'''
def update_summary_aggs(dct_agg,count_val,column, clicked,  target_fields):
    dct_agg['Min_'+target_fields[clicked]+'_'+column]=min(dct_agg['Min_'+target_fields[clicked]+'_'+column],count_val)
    dct_agg['Max_'+target_fields[clicked]+'_'+column]=max(dct_agg['Max_'+target_fields[clicked]+'_'+column],count_val)
    dct_agg['Mean_'+target_fields[clicked]+'_'+column]=dct_agg['Mean_'+target_fields[clicked]+'_'+column]* dct_agg['Count_'+target_fields[clicked]+'_'+column]
    dct_agg['Count_'+target_fields[clicked]+'_'+column]+=1
    return dct_agg


''' Function to calculate similarity between different categorical hashes'''
def update_similarity(hashable_fields,dct_row, dct_agg):

    for i in range(len(hashable_fields)):
        for j in range(i+1, len(hashable_fields)):
            field1=dct_row[hashable_fields[i]]
            field2=dct_row[hashable_fields[j]]
            hash1=hashing(field1)
            hash2=hashing(field2)
            similarity=cosine_similarity(hash1, hash2)[0][0]
    #print 'similarity_'+str(hashable_fields[i])+'_'+str(hashable_fields[j])
            dct_row['Similarity_'+str(hashable_fields[i])+'_'+str(hashable_fields[j])]=similarity                               
    return dct_row
    

def readFile(filename):
    count_cols=['Count_'+str(i) for i in range(1,num_count_features+1)]
    categorical_cols=['Categorical_'+str(i) for i in range(1,num_categorical_features+1)]
    header=['clicked']+count_cols+categorical_cols
    target_fields={'1':'click','0':'noclick'}
    header
    row_dict={}
    dct_agg=init_agg_dict(target_fields, count_cols)
    with open(filename,'r') as fin:
        line_count=0
        csv_r=csv.DictReader(fin, fieldnames=header,delimiter='\t')
        
        for row in csv_r:
            #print row
            dct_row={}

            clicked=row['clicked'] # Clicked or not clicked
            for i in range(len(count_cols)):
                count_val=int(row[count_cols[i]] if row[count_cols[i]]!='' else 0)
                dct_agg=update_summary_aggs(dct_agg, count_val,count_cols[i], clicked, target_fields)
            # Handling categorical features
            hashable_fields=categorical_cols
            row=update_similarity(hashable_fields, row)
            row.update(dct_agg)#merging the dictionaries
            row_dict[line_count-1]=row# Accounting for header
            line_count+=1
            print 'line_count {}'.format(line_count),' ', 
    fout=open('out.txt','w')
    strout=','.join(each  for each in row_dict[0].keys())
    fout.write(strout+'\n')
    for each in row_dict:
        dct=row_dict[each]
        #print dct
        strout=','.join(str(dct[each]) for each in dct)
        fout.write(strout+'\n')
    fout.close()
if __name__=='__main__':
    readFile(sys.argv[1])
