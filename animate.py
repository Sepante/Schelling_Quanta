from main import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

pos = nx.circular_layout(G)
fig = plt.figure(figsize = (5,5))
ax = fig.add_subplot(1,1,1)

def display():
    nx.draw_networkx_edges(G, pos = pos, ax = ax, alpha = 0.5)
    ax.axis('off')
    pos_array = np.array( list( pos.values() ) )
    limits = 1.1*np.array([pos_array.min(), pos_array.max()])
    ax.set_ylim( limits )
    ax.set_xlim( limits )
    
    unoccupied = np.where(agents['ethn'] == -1)[0]
    nx.draw_networkx_nodes(G, pos = pos, ax = ax, nodelist=unoccupied, node_color ='w', edgecolors = 'black')
    
    unsat_0 = np.where( np.all([agents['similar_neigh'] < sat_threshold, agents['ethn'] == 0], 0) )[0]
    nx.draw_networkx_nodes(G, pos = pos, ax = ax, nodelist=unsat_0, node_color ='b', edgecolors = 'black', node_shape = 'X')
    
    sat_0 = np.where( np.all([agents['similar_neigh'] >= sat_threshold, agents['ethn'] == 0], 0) )[0]
    nx.draw_networkx_nodes(G, pos = pos, ax = ax, nodelist=sat_0, node_color ='b', edgecolors = 'black', node_shape = 'o')
    
    unsat_1 = np.where( np.all([agents['similar_neigh'] < sat_threshold, agents['ethn'] == 1], 0) )[0]
    nx.draw_networkx_nodes(G, pos = pos, ax = ax, nodelist=unsat_1, node_color ='r', edgecolors = 'black', node_shape = 'X')
    
    sat_1 = np.where( np.all([agents['similar_neigh'] >= sat_threshold, agents['ethn'] == 1], 0) )[0]
    nx.draw_networkx_nodes(G, pos = pos, ax = ax, nodelist=sat_1, node_color ='r', edgecolors = 'black', node_shape = 'o')
    return fig

def animate(t):
    ax.clear()
    print(t)
    
    update_satisifaction(G)
    fig = display()
    
    move_candidate(agents)
    
    return fig



ani = animation.FuncAnimation(fig, animate, save_count=10)
ani.save( 'animation.GIF', writer = 'imagemagick', fps = 1, dpi = 100 )