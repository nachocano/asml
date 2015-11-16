
# coding: utf-8

# In[ ]:

import os
import sys
import random
from collections import defaultdict


# In[ ]:

os.chdir('F://CSE544_Project//')


# In[ ]:




# In[ ]:

def init_pagerank(N):
    page_rank_map= defaultdict( lambda : 1.0/N) 
    return page_rank_map
# The default page rank is 1/N where N is the number of nodes. Right now, just passing a default value. 
#TODO: What should be the default value in the incremental version


# In[ ]:

def read_index(filename):
    website_index_dict={}
    index_website_dict={}
    with open(filename,'r') as indexfile:
        for line in indexfile:
            filename, fileindex=line.split()
            website_index_dict[filename]=fileindex
            index_website_dict[fileindex]=filename
    return website_index_dict,index_website_dict


# In[ ]:

def read_arc(filename):
    arc_dict=defaultdict(list)
    with open(filename, 'r') as arcfile:
        for line in arcfile:
          if line.strip()!='':
#             print line
            src, dest=line.split(' ')
            src=src.strip()
            dest=dest.strip()
            arc_dict[src].append(dest)
#     print 'Inside read_arc', arc_dict
    return arc_dict


# In[ ]:

def incoming_nodes_list(arc_dict, iid):
    in_list=[]
    for key in arc_dict:
#         print 'iid={}, key={}, arc_dict[key]={}'.format(iid, key, arc_dict[key])
        if iid in arc_dict[key]:
            in_list.append(key)
    return list(set(in_list))


# In[ ]:

def outgoing_nodes_list(arc_dict, iid):
    return arc_dict[iid]


# In[ ]:

def calculate_pagerank(no_of_iter,no_of_nodes, page_rank_map, arc_map, damping):
    for iter in range(no_of_iter):
        rand_node=str(random.randint(0,no_of_nodes-1))# Assuming consecutive node ids
        print 'Rand_Node={}'.format(rand_node)
        incoming_vector=incoming_nodes_list(arc_map,rand_node) # The list of nodes having incoming links to the rand_node
#         print 'Incoming_vector={}'.format(incoming_vector)
        outgoing_vector=outgoing_nodes_list(arc_map, rand_node)
#         print 'Outgoing_vector={}'.format(outgoing_vector)
        sum=0
        out_length=len(outgoing_vector)
        in_length=len(incoming_vector)
        print 'Length of incoming vector ={}, outgoing vector={}'.format(in_length, out_length)
        if in_length!=0 and out_length!=0:
            for in_node in incoming_vector:
                sum+=page_rank_map[in_node]/float(len(outgoing_nodes_list(arc_map, in_node)))
            sum*=damping
            page_rank = sum+((1.0-damping)/len(page_rank_map))
            page_rank_map[rand_node]=page_rank
    return page_rank_map


# In[ ]:

def print_page_ranks(page_rank_map):
    for iid, pr in page_rank_map.items():
        print iid,' ', pr


# In[ ]:

def main():
    website_index_dict,index_website_dict=read_index('simple_nodes.txt')
    arcs_map=read_arc('simple_arcs.txt')
    page_rank_map=init_pagerank(len(website_index_dict.keys()))
    page_rank_map=calculate_pagerank(10,len(website_index_dict.keys()), page_rank_map, arcs_map,0.5)
    return page_rank_map


# In[ ]:

page_rank_map=main()


# In[ ]:

page_rank_map


# In[ ]:



