import pandas as pd
import numpy as np
from anytree import Node, RenderTree

def ancestor_map(df):
	dt = {}
	for index, row in df.iterrows():
		dt[row['name']] = row['ancestors'].split(',')
	return dt

def get_node(node_name, nodes_list):
    for n in nodes_list:
        if n.name == node_name:
            return n
    else:
        return 

def build_tree(dt):
	nodes = []
	node_names = []
	root = Node("artificialintelligence")

	for key, value in dt.items():
	    if (value == ["blank"]) | (value == ['artificialintelligence']):
	        curr = Node(key, parent = root)
	        
	        # add to existing nodes
	        node_names.append(key)
	        nodes.append(curr)
	    
	    else:
	        new_nodes = [i for i in value if (i != 'artificialintelligence') & (i not in node_names)]
	        has_parents = list(set(value) - set(new_nodes))
	      
	        for h in has_parents:
	            parent_n = get_node(h, nodes)
	            curr = Node(key, parent = parent_n)
	            
	            # add to existing nodes
	            node_names.append(key)
	            nodes.append(curr)
	            
	        
	        for v in new_nodes:
	            # creae nodes
	            # each v is a potential parent
	            parent_n = get_node(v, nodes)
	            curr = Node(key, parent = Node(key, parent = parent_n))
	            
	            # add to existing nodes
	            node_names.append(key)
	            nodes.append(curr)
	return root

def display_tree(root):
	for pre, fill, node in RenderTree(root):
		print("%s%s" % (pre, node.name))