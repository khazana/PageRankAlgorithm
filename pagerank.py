
import numpy as np


#include this function in simple_web_graph.py or   focused_webgraph.py with numpy and rank_dict = {}
def compute_rank():
    node_set = list(set().union(incoming_dict.keys(),outgoing_dict.keys()))
    surprise_parameter = 0.15
    previous_rank = {}
    rank_dict = {}
    keys_links = incoming_dict.keys()
    for node in node_set:
        previous_rank[node]= 1 / len(node_set)
        rank_dict[node] = 1 / len(node_set)
    j = 0
    while j < 250:
        for key in keys_links:
            rank_dict[key] = 0
            for value in incoming_dict[key]:
                rank_dict[key] = rank_dict[key] + previous_rank[value]/len(outgoing_dict.get(value))
            rank_dict[key] = rank_dict[key]*(1 - surprise_parameter) + (surprise_parameter/len(node_set))
        sum1 = 0.0
        for n in  node_set:
            s =  rank_dict[n]
            sum1 = sum1 + s
        print("L2 norm value:",np.linalg.norm(list(rank_dict.values()),ord=2))
        print("Page rank sum:",sum1)
        print('\n')
        if(np.linalg.norm(list(rank_dict.values()),ord=2) - np.linalg.norm(list(previous_rank.values()),ord=2) > 0.0005):
            for key in rank_dict:
                previous_rank[key] = rank_dict[key]
        else:
            for key in rank_dict:
                previous_rank[key] = rank_dict[key]
            j = j + 1
    sorted_by_value = sorted(rank_dict.items(), key=lambda kv: (-kv[1],kv[0]))
                    
                    
                    
            
        
#function to get descending indegree list
def sort_indegree():
    length = {}
    for key in incoming_dict:
        l = len(list(incoming_dict[key]))
        length[key] = l
    sorted_list = sorted(length.items(), key=lambda kv: (-kv[1],kv[0]))
     
        
    
    
     
        
        
        
      
    
    
     
        
        
    
    
  



    


 
    
    
    
  


 
    
    
    
    
  


