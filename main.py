import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

n = 40 #population size
p = 4 / n #connectivity probability between the nodes (used in erdos renyi graph)
G = nx.erdos_renyi_graph(n, p)
T = 10 #maximum time-steps
sat_threshold = 0.5 #satisfaction threshold
first_ethn_population = int(n * 0.48 ) #percentage of agents of the first ethnicity
#nx.draw(G)

agents = np.recarray((n), dtype=[('ethn', int), ('similar_neigh', float)]) 



agents['similar_neigh'] = 0

#init
agents['ethn'][:first_ethn_population] = 0
agents['ethn'][first_ethn_population : 2 * first_ethn_population ] = 1
agents['ethn'][2 * first_ethn_population:] = -1 #vacant nodes

def update_satisifaction(G):
    for i in range( len(G) ):        
        my_type = agents['ethn'][i]
        if my_type == -1:
            return -1
        else:
            neighbors = np.array( list(G.neighbors(i) ))
            #print(neighbors)
            occupied_neighbors = neighbors[  agents['ethn'][neighbors] != -1  ]
            #print(occupied_neighbors)
            desired_neighbors = np.sum( agents['ethn'][occupied_neighbors] == my_type )
            if len(neighbors) == 0:
                agents['similar_neigh'][i] = 1
            else:
                agents['similar_neigh'][i] = desired_neighbors / len(neighbors)


#agents['similar_neigh'][ agents['similar_neigh'] < sat_threshold ]
def moving_candidate(agents):
    unsat_arr = np.where( np.all([agents['similar_neigh'] < sat_threshold, agents['ethn'] != -1], 0) )[0]
    vacant_arr = np.where( agents['ethn'] == -1 )[0]
    
    unsat_candidate = np.random.choice(unsat_arr)
    vacant_candidate = np.random.choice(vacant_arr) 
    #print(unsat_candidate, vacant_candidate)
    return unsat_candidate, vacant_candidate

def move_candidate(agents):
    unsat_cand,vacant_cand = moving_candidate(agents)
    agents['ethn'][unsat_cand], agents['ethn'][vacant_cand] =\
     agents['ethn'][vacant_cand], agents['ethn'][unsat_cand]



for t in range(T):
    update_satisifaction(G)
    move_candidate(agents)
#    #print( agents['ethn'] )
